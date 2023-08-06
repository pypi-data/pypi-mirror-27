from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
import uuid


class XLSImportProfile(models.Model):
    UNAVAILABLE_ACTION_CHOICES = (
        ('', _('Do nothing')),
        ('set-status', _('Set specified status')),
        ('unpublish', _('Remove from site (unpublish)')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255, unique=True)
    language = models.CharField(_('Language'), max_length=10)

    first_row_as_labels = models.BooleanField(
        _('First row as labels'), default=True,
        help_text=_('Get column labels from the first row.')
    )

    default_product_type = models.ForeignKey(
        'pcart_catalog.ProductType', verbose_name=_('Default product type'))
    default_collection = models.ForeignKey(
        'pcart_catalog.Collection', verbose_name=_('Default collection'))

    unavailable_action = models.CharField(
        _('Unavailable action'), default='',
        max_length=50, blank=True,
        choices=UNAVAILABLE_ACTION_CHOICES,
        help_text=_('Choose the action to do for products which are not available in the price list.'),
    )
    unavailable_status = models.ForeignKey(
        'pcart_catalog.ProductStatus',
        verbose_name=_('Unavailable status'),
        related_name='xls_import_profiles',
        blank=True, null=True,
        help_text=_('If not set the status with minimal weight will be used.'),
        on_delete=models.CASCADE,
    )

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('XLS Import profile')
        verbose_name_plural = _('XLS Import profiles')
        ordering = ['title']

    def __str__(self):
        return self.title


class XLSColumn(models.Model):
    DESTINATION_CHOICES = (
        ('product_type', _('Product type')),
        ('collection', _('Collection')),
        ('extra_collection', _('Extra collection')),
        ('vendor', _('Vendor')),
        ('product', _('Product')),
        ('id', _('ID')),
        ('external_id', _('External ID')),
        ('product_image', _('Product image')),
        ('product_property', _('Product property')),
        ('price', _('Price')),
        ('quantity', _('Quantity')),
        ('product_status', _('Status')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        XLSImportProfile, verbose_name=_('Import profile'),
        related_name='columns',
    )
    column_index = models.CharField(_('Column index'), max_length=100, blank=True, default='')
    use_column_label = models.BooleanField(
        _('Use column label'), default=True,
        help_text=_('If checked "Column index" is related to column label, otherwise it is a column number.')
    )
    destination = models.CharField(
        _('Destination'), max_length=100, choices=DESTINATION_CHOICES,
        help_text=_('See documentation for supported values.')
    )
    sub_destination = models.CharField(_('Sub-destination'), max_length=100, default='', blank=True)

    function = models.TextField(
        _('Function'), default='', blank=True,
        help_text=_('Use P-Cart Script for implementing complex logic.')
    )

    class Meta:
        verbose_name = _('XLS column')
        verbose_name_plural = _('XLS columns')
        ordering = ['column_index']

    def __str__(self):
        return self.column_index

    def get_destination(self):
        if self.sub_destination:
            return '%s:%s' % (self.destination, self.sub_destination)
        else:
            return self.destination

def generate_price_list_filename(instance, filename):
    """
    Returns a price list file name.
    """
    ext = filename.split('.')[-1]
    url = 'import/xls-price-lists/%s/%s.%s' % (
        instance.id, str(instance.id).replace('-', ''), ext)
    return url


class XLSPriceList(models.Model):
    XLS_PRICE_LIST_STATUS_CHOICES = (
        ('new', _('New')),
        ('processing', _('Processing')),
        ('success', _('Success')),
        ('with_errors', _('With errors')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        XLSImportProfile, verbose_name=_('Import profile'),
        related_name='price_lists',
    )
    file = models.FileField(
        _('Price list'), upload_to=generate_price_list_filename,
        help_text=_('Price list file.'),
    )

    status = models.CharField(
        _('Status'), default='new', max_length=70, choices=XLS_PRICE_LIST_STATUS_CHOICES)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('XLS Price list')
        verbose_name_plural = _('XLS Price lists')
        ordering = ['-added']

    def __str__(self):
        return str(self.file)

    @staticmethod
    def cell_to_str(cell):
        """Returns a cell value as string."""
        if cell.ctype == 1:  # string
            return str(cell.value).strip()
        elif cell.ctype == 2:  # number
            if cell.value == int(cell.value):
                return str(int(cell.value))
            else:
                return str(float(cell.value))
        else:
            return str(cell.value)

    def load_data(self, limit=50):
        import xlrd
        from pcart_script.interpreter import LispInterpreter
        workbook = xlrd.open_workbook(self.file.path)
        sheet = workbook.sheet_by_index(0)

        labels = None
        start_row = 0
        if self.profile.first_row_as_labels:
            labels = [self.cell_to_str(x) for x in sheet.row(0)]
            start_row = 1
        stop_row = sheet.nrows

        columns = self.profile.columns.all()

        result = []
        for i in range(start_row, stop_row):
            if limit is not None and i > limit:
                break

            row = [self.cell_to_str(x) for x in sheet.row(i)]
            chunk = []

            for col in columns:
                if col.column_index == '':
                    index = None
                elif self.profile.first_row_as_labels and col.use_column_label:
                    index = labels.index(col.column_index)
                else:
                    index = int(col.column_index)

                if col.function:
                    _value = row[index] if index is not None else ''
                    if labels:
                        _columns = {k: v for k, v in zip(labels, row)}
                    else:
                        _columns = {k: v for k, v in zip(range(len(row)), row)}
                    _result = LispInterpreter(
                        code=col.function,
                        globals={
                            'value': _value,
                            'columns': _columns,
                        },
                    ).execute()
                    if _result is None:
                        # Ignore line if function returned #nil
                        chunk = []
                        break
                    chunk.append(_result)
                else:
                    chunk.append(row[index] if index is not None else '')

            if chunk:
                result.append(chunk)

        meta = {
            'labels': labels,
            'columns': columns,
        }

        return result, meta

    def process(self):
        from decimal import Decimal
        from urllib.error import URLError
        from pcart_catalog.models import (
            Vendor,
            Product,
            ProductImage,
            ProductStatus,
            ProductType,
            Collection,
        )
        from pcart_core.utils import get_unique_slug

        self.status = 'processing'
        self.save()

        status_available = ProductStatus.objects.order_by('-weight').first()
        status_unavailable = self.profile.unavailable_status or ProductStatus.objects.order_by('-weight').last()

        try:
            result, meta = self.load_data(limit=None)

            columns = meta['columns']

            collections_ids_set = set()
            products_ids = list()

            for item in result:
                chunk = {k.get_destination(): v for k, v in zip(columns, item)}

                try:
                    if 'id' in chunk:
                        product = Product.objects.get(pk=chunk['id'])
                    elif 'external_id' in chunk:
                        product = Product.objects.get(external_id=chunk['external_id'])
                    else:
                        product = Product()
                        if 'id' in chunk:
                            product.id = chunk['id']
                        if 'external_id' in chunk:
                            product.external_id = chunk['external_id']
                except Product.DoesNotExist:
                    product = Product()
                    if 'id' in chunk:
                        product.id = chunk['id']
                    if 'external_id' in chunk:
                        product.external_id = chunk['external_id']

                product.set_current_language(self.profile.language)
                product.product_type = self.profile.default_product_type

                if 'product_type' in chunk:
                    try:
                        p_type = ProductType.objects.translated(
                            self.profile.language,
                            title=chunk['product_type']).get()
                        product.product_type = p_type
                    except ProductType.DoesNotExist:
                        XLSImportHistory.objects.create(
                            price_list=self, success=False,
                            message='Ignore row\n%s\nProduct type "%s" not found.' % (chunk, chunk['product_type']),
                        )
                        continue

                product.title = chunk.get('product:title')
                if not product.title:
                    XLSImportHistory.objects.create(
                        price_list=self, success=False,
                        message='Ignore row\n%s\nProduct title is empty.' % chunk,
                    )
                    continue

                if 'vendor' in chunk:
                    try:
                        vendor = Vendor.objects.translated(
                            self.profile.language,
                            title=chunk['vendor']).get()
                    except Vendor.DoesNotExist:
                        vendor = Vendor()
                        vendor.set_current_language(self.profile.language)
                        vendor.title = chunk['vendor']
                        vendor.slug = get_unique_slug(chunk['vendor'], Vendor)
                        vendor.save()
                    product.vendor = vendor

                if not product.slug:
                    product.slug = get_unique_slug(product.title, Product)
                product.description = chunk.get('product:description', '')
                product.sku = chunk.get('product:sku', '')
                product.barcode = chunk.get('product:barcode', '')
                product.weight = float(chunk.get('product:weight', 0.0))

                _props = {}
                for c in chunk.keys():
                    if c.startswith('product_property:'):
                        _props[c[17:]] = chunk[c]
                product.properties = _props

                if 'quantity' in chunk:
                    _quantity = int(chunk['quantity'])
                    product.quantity = _quantity
                    if _quantity > 0:
                        product.status = status_available
                    else:
                        product.status = status_unavailable
                else:
                    product.status = status_available

                # Fix visibility back depends the settings
                if self.profile.unavailable_action != '':
                    if self.profile.unavailable_action == 'set-status' and 'quantity' not in chunk:
                        # If quantity is not in price list this particular block will work
                        product.status = status_available
                    elif self.profile.unavailable_action == 'unpublish':
                        product.published = True

                product.price = Decimal(chunk.get('price', '0.0'))
                product.save()

                if 'collection' in chunk:
                    try:
                        collection = Collection.objects.translated(
                            self.profile.language,
                            title=chunk['collection']).get()
                        product.collections = [collection]
                        collections_ids_set.add(collection.id)
                    except Collection.DoesNotExist:
                        XLSImportHistory.objects.create(
                            price_list=self, success=False,
                            message='Ignore row\n%s\nCollection "%s" not found.' % (chunk, chunk['collection']),
                        )
                        continue
                else:
                    product.collections = [self.profile.default_collection]
                    collections_ids_set.add(self.profile.default_collection_id)

                images_links = []
                im_keys = []
                for im in chunk:
                    if im.startswith('product_image:'):
                        im_keys.append(im.split(':'))
                im_keys = sorted(im_keys, key=lambda x: int(x[1]))
                # print(im_keys)
                for k in im_keys:
                    # print(k)
                    images_links.append(chunk['{}:{}'.format(*k)])

                images_for_delete = product.images.exclude(download_link__in=images_links)
                if images_for_delete:
                    images_for_delete.delete()

                available_images_links = list(product.images.values_list('download_link', flat=True))
                for im in images_links:
                    if im and im not in available_images_links:
                        # print(im)
                        try:
                            image = ProductImage()
                            image.set_current_language(self.profile.language)
                            image.title = ''
                            image.product = product
                            image.download_link = im
                            image.save()
                        except URLError:
                            XLSImportHistory.objects.create(
                                price_list=self, success=False, product=product,
                                message='Image download error\n%s\nCannot download image "%s".' % (chunk, im),
                            )
                        except Exception as e:
                            XLSImportHistory.objects.create(
                                price_list=self, success=False, product=product,
                                message='Image download error\n%s\n%s' % (chunk, e),
                            )

                product.save()

                products_ids.append(product.id)

                XLSImportHistory.objects.create(
                    price_list=self, success=True, product=product,
                    message='%s' % chunk,
                )

            # Do something with unavailable products
            if self.profile.unavailable_action != '':
                collections = Collection.objects.filter(id__in=list(collections_ids_set))
                shop_products_ids_set = set(
                    Product.objects.filter(collections__in=collections).values_list('id', flat=True))
                products_ids_set = set(products_ids)
                non_available_products_ids = shop_products_ids_set - products_ids_set
                non_available_products = Product.objects.filter(id__in=list(non_available_products_ids))
                if self.profile.unavailable_action == 'set-status':
                    non_available_products.update(status=status_unavailable)
                elif self.profile.unavailable_action == 'unpublish':
                    non_available_products.update(published=False)

            self.status = 'success'
            self.save()
        except Exception as e:
            self.status = 'failed'
            self.save()
            raise e


@receiver(post_delete, sender=XLSPriceList)
def price_list_post_delete_listener(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


class XLSImportHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price_list = models.ForeignKey(XLSPriceList, verbose_name=_('Price list'), related_name='history')
    product = models.ForeignKey(
        'pcart_catalog.Product', verbose_name=_('Product'),
        related_name='xls_import_history', null=True, blank=True)

    success = models.BooleanField(_('Success'), default=True)
    message = models.TextField(_('Message'), default='', blank=True)

    added = models.DateTimeField(_('Added'), auto_now_add=True)

    class Meta:
        verbose_name = _('XLS Import history')
        verbose_name_plural = _('XLS Import history')
        ordering = ['-added']

    def __str__(self):
        return '%s - %s' % (self.price_list, self.product)


class YMLImportProfile(models.Model):
    UNAVAILABLE_ACTION_CHOICES = (
        ('', _('Do nothing')),
        ('set-status', _('Set specified status')),
        ('unpublish', _('Remove from site (unpublish)')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255, unique=True)
    language = models.CharField(_('Language'), max_length=10)

    url = models.CharField(_('URL'), max_length=255)

    active = models.BooleanField(_('Active'), default=True)
    last_download = models.DateTimeField(_('Last download'), blank=True, null=True)
    check_interval = models.PositiveIntegerField(
        _('Check interval'), default=24,
        help_text=_('The interval between data downloading in hours.'))

    unavailable_action = models.CharField(
        _('Unavailable action'), default='',
        max_length=50, blank=True,
        choices=UNAVAILABLE_ACTION_CHOICES,
        help_text=_('Choose the action to do for products which are not available in the price list.'),
    )
    unavailable_status = models.ForeignKey(
        'pcart_catalog.ProductStatus',
        verbose_name=_('Unavailable status'),
        related_name='yml_import_profiles',
        blank=True, null=True,
        help_text=_('If not set the status with minimal weight will be used.'),
        on_delete=models.CASCADE,
    )

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('YML Import profile')
        verbose_name_plural = _('YML Import profiles')
        ordering = ['title']

    def __str__(self):
        return self.title

    def try_to_check_yml(self):
        """
        Check if there is a time for check and download new version of YML file.
        """
        from django.utils import timezone
        from datetime import timedelta

        if self.last_download is None:
            self.download()
        else:
            _now = timezone.now()
            _next_check_time = self.last_download + timedelta(hours=self.check_interval)
            if _now >= _next_check_time:
                self.download()

    def download(self, add_price_list_to_db: bool = True) -> str:
        from django.core.files import File
        from django.utils import timezone
        import urllib.request
        import urllib.parse
        import os

        o = urllib.parse.urlparse(self.url)
        local_filename, headers = urllib.request.urlretrieve(self.url)
        if add_price_list_to_db and local_filename:
            # Update the date of last download
            self.last_download = timezone.now()
            self.save()

            price_list = YMLPriceList(profile=self)
            price_list.file.save(
                os.path.basename(o.path),
                File(open(local_filename, 'rb')),
                save=False,
            )
            price_list.save()

        return local_filename


class YMLImportCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255, unique=True)
    profile = models.ForeignKey(
        YMLImportProfile, verbose_name=_('Import profile'),
        related_name='import_categories',
    )
    default_product_type = models.ForeignKey(
        'pcart_catalog.ProductType', verbose_name=_('Default product type'), null=True, blank=True)
    default_collection = models.ForeignKey(
        'pcart_catalog.Collection', verbose_name=_('Default collection'), null=True, blank=True)

    product_type_function = models.TextField(
        _('Product type function'), default='', blank=True,
        help_text=_('Use P-Cart Script for implementing complex logic.')
    )
    collection_function = models.TextField(
        _('Collection function'), default='', blank=True,
        help_text=_('Use P-Cart Script for implementing complex logic.')
    )

    class Meta:
        verbose_name = _('YML Import category')
        verbose_name_plural = _('YML Import categories')
        ordering = ['title']

    def __str__(self):
        return self.title


class YMLImportProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        YMLImportCategory, verbose_name=_('YML Import category'),
        related_name='properties',
        on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=255)
    rename_to = models.CharField(_('Rename to'), max_length=255, blank=True, default='')

    class Meta:
        verbose_name = _('YML Import property')
        verbose_name_plural = _('YML Import properties')
        ordering = ['title']
        unique_together = ('category', 'title')

    def __str__(self):
        return self.title


def generate_yml_price_list_filename(instance, filename):
    """
    Returns a price list file name.
    """
    ext = filename.split('.')[-1]
    url = 'import/yml-price-lists/%s/%s.%s' % (
        instance.id, str(instance.id).replace('-', ''), ext)
    return url


class YMLPriceList(models.Model):
    YML_PRICE_LIST_STATUS_CHOICES = (
        ('new', _('New')),
        ('processing', _('Processing')),
        ('success', _('Success')),
        ('with_errors', _('With errors')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        YMLImportProfile, verbose_name=_('Import profile'),
        related_name='price_lists',
    )
    file = models.FileField(
        _('Price list'), upload_to=generate_yml_price_list_filename,
        help_text=_('Price list file.'),
    )

    status = models.CharField(
        _('Status'), default='new', max_length=70, choices=YML_PRICE_LIST_STATUS_CHOICES)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('YML Price list')
        verbose_name_plural = _('YML Price lists')
        ordering = ['-added']

    def __str__(self):
        return str(self.file)

    @staticmethod
    def run_code(code, attrs=None):
        from pcart_script.interpreter import LispInterpreter
        if attrs is None:
            attrs = {}
        _result = LispInterpreter(code=code, globals=attrs).execute()
        return _result

    def load_data(self, limit: int = 50, ignore_products: bool = False):
        from lxml import etree
        from django.core.files.storage import default_storage

        xml = etree.parse(default_storage.open(self.file.path, 'rb'))
        root = xml.getroot()

        categories = root.xpath('shop/categories/category')
        categories_data = []
        for c in categories:
            categories_data.append({
                'id': dict(c.items())['id'],
                'title': c.text,
            })

        offers = root.xpath('shop/offers/offer')
        products_data = []
        if not ignore_products:
            for p in offers:
                _attrs = dict(p.items())
                chunk = {
                    'external_id': _attrs['id'],
                    'available': _attrs['available'],
                    'category_id': p.xpath('categoryId')[0].text,
                    'title': p.xpath('name')[0].text,
                    'vendor': p.xpath('vendor')[0].text,
                    'description': p.xpath('description')[0].text,
                    'quantity': p.xpath('quantity_in_stock')[0].text,
                    'price': p.xpath('price')[0].text,
                    'images': [x.text for x in p.xpath('picture')],
                    'properties': [(dict(x.items())['name'], x.text) for x in p.xpath('param')],
                }
                # if self.profile.property_function:
                #     chunk.update({
                #         'properties_f': {},
                #     })

                products_data.append(chunk)

        return categories_data, products_data

    def process(self):
        from decimal import Decimal
        from urllib.error import URLError
        from pcart_catalog.models import (
            Vendor,
            Product,
            ProductImage,
            ProductStatus,
            ProductType,
            Collection,
        )
        from pcart_core.utils import get_unique_slug

        self.status = 'processing'
        self.save()

        status_available = ProductStatus.objects.order_by('-weight').first()
        status_unavailable = ProductStatus.objects.order_by('-weight').last()

        try:
            categories, products = self.load_data(limit=None)

            collections_ids_set = set()
            products_ids = list()

            for c in categories:
                try:
                    _yml_category = YMLImportCategory.objects.get(
                        pk=c['id'], profile=self.profile)
                    if _yml_category.title != c['title']:
                        _yml_category.title = c['title']
                        _yml_category.save()
                except YMLImportCategory.DoesNotExist:
                    YMLImportCategory.objects.create(
                        pk=c['id'],
                        title=c['title'],
                        profile=self.profile,
                    )

            yml_categories = {
                str(x.id): x for x in YMLImportCategory.objects.all().prefetch_related('properties')}

            product_ids = []

            for p in products:
                if p['category_id'] in yml_categories:
                    _yml_category = yml_categories[p['category_id']]

                    product_type = _yml_category.default_product_type
                    collection = _yml_category.default_collection

                    if _yml_category.product_type_function:
                        product_type_f = self.run_code(_yml_category.product_type_function, p)
                        if product_type_f:
                            try:
                                product_type = ProductType.objects.translated(
                                    self.profile.language,
                                    title=product_type_f).get()
                            except ProductType.DoesNotExist:
                                product_type = None

                    if _yml_category.collection_function:
                        collection_f = self.run_code(_yml_category.collection_function, p)
                        if collection_f:
                            try:
                                collection = Collection.objects.translated(
                                    self.profile.language,
                                    title=collection_f).get()
                            except Collection.DoesNotExist:
                                collection = None

                    # Save properties to import settings
                    _props_names = {}
                    for item in p['properties']:
                        try:
                            _prop = _yml_category.properties.get(title=item[0])
                            _props_names[item[0]] = _prop.rename_to
                        except YMLImportProperty.DoesNotExist:
                            _prop = YMLImportProperty(
                                category=_yml_category,
                                title=item[0],
                            )
                            _prop.save()
                            _props_names[item[0]] = ''

                    try:
                        product = Product.objects.get(external_id=p['external_id'])
                    except Product.DoesNotExist:
                        product = Product()

                    if product_type is not None:
                        product.set_current_language(self.profile.language)
                        product.product_type = product_type
                        product.title = p['title']

                        if p['vendor']:
                            try:
                                vendor = Vendor.objects.translated(
                                    self.profile.language,
                                    title=p['vendor']).get()
                            except Vendor.DoesNotExist:
                                vendor = Vendor()
                                vendor.set_current_language(self.profile.language)
                                vendor.title = p['vendor']
                                vendor.slug = get_unique_slug(p['vendor'], Vendor)
                                vendor.save()
                            product.vendor = vendor

                        if not product.slug:
                            product.slug = get_unique_slug(product.title, Product)

                        product.description = p['description']
                        product.properties = {
                            _props_names.get(k) or k: v for k, v in p['properties']}

                        # TODO: review it later
                        _quantity = int(p['quantity'])
                        product.quantity = _quantity
                        if _quantity > 0:
                            product.status = status_available
                        else:
                            product.status = status_unavailable

                        product.price = Decimal(p['price'])
                        product.save()

                        if collection:
                            product.collections = [collection]
                        else:
                            YMLImportHistory.objects.create(
                                price_list=self, success=False,
                                message='Ignore row\n%s\nCollection not found.' % p,
                            )
                            continue

                        product_ids.append({
                            'external_id': p['external_ids'],
                            'id': product.id,
                            'collection_id': collection.id if collection else None,
                            'product_type_id': product_type.id if product_type else None,
                        })
                    else: # product_type is None
                        YMLImportHistory.objects.create(
                            price_list=self, success=False,
                            message='Ignore row\n%s\nProduct type is empty.' % p,
                        )
                        continue

            # print(product_ids)

            self.status = 'success'
            self.save()
        except Exception as e:
            self.status = 'failed'
            self.save()
            raise e



@receiver(post_delete, sender=YMLPriceList)
def price_list_post_delete_listener(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


class YMLImportHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price_list = models.ForeignKey(YMLPriceList, verbose_name=_('Price list'), related_name='history')
    product = models.ForeignKey(
        'pcart_catalog.Product', verbose_name=_('Product'),
        related_name='yml_import_history', null=True, blank=True)

    success = models.BooleanField(_('Success'), default=True)
    message = models.TextField(_('Message'), default='', blank=True)

    added = models.DateTimeField(_('Added'), auto_now_add=True)

    class Meta:
        verbose_name = _('YML Import history')
        verbose_name_plural = _('YML Import history')
        ordering = ['-added']

    def __str__(self):
        return '%s - %s' % (self.price_list, self.product)


