from collections import OrderedDict

from .base import export, Table as BaseTable
from .etl_tracking import STAGING_SCHEMA, TASKS_NAME

tables = OrderedDict()


class Table(BaseTable):
    source = 'snapfulfil'

    @property
    def from_clause(self):
        super_ = super().from_clause
        return f"{super_}, LATERAL FLATTEN(INPUT => t.contents) _shipments"

    def select(self):
        cols = ',\n\t\t'.join(
            f"STRIP_NULL_VALUE(GET(_{self.name}.value, '{col}'))"
            for col, _ in self.column_spec
        )
        return f'''
            SELECT
                {cols},
                t.s3_path
            FROM
                {self.from_clause}
            WHERE
                {self.where_clause}
        '''

    @property
    def merge_source_name(self):
        return f'{STAGING_SCHEMA}._dedupe_snapfulfil_{self.name}'

    @property
    def merge_source_view(self):
        cols = [c for c, _ in self.full_column_spec(False)]
        pk = self.merge_join
        keys = ', '.join(f'r.{k}' for k in pk)
        selectables = ',\n\t'.join(
            f'r.{c}' if c in pk else (
                f'FIRST_VALUE(r.{c}) IGNORE NULLS OVER'
                f' (PARTITION BY {keys} ORDER BY t.created_at DESC)'
            ) for c in cols
        )
        spec = ', '.join(cols)
        return f'''
            CREATE OR REPLACE VIEW {self.merge_source_name} ({spec}) AS
            SELECT DISTINCT
                {selectables}
            FROM
                {self.staging_tablename} r
                JOIN {TASKS_NAME} t
                    ON t.table_name = '{self.name}' AND t.s3_path = r.s3_path
        '''

    merge_updates = property(BaseTable._update_all)


@export(tables)
class Shipments(Table):
    name = 'shipments'
    _flattened_table = 'shipments'
    column_spec = (
        ('ShipmentId', 'VARCHAR PRIMARY KEY'),
        ('BizId', 'VARCHAR'),
        ('BizSalesOrder', 'VARCHAR'),
        ('Status', 'VARCHAR'),
        ('OrderType', 'VARCHAR'),
        ('OrderClass', 'VARCHAR'),
        ('CustomerId', 'VARCHAR'),
        ('BizCustomerId', 'VARCHAR'),
        ('CustomerGroup', 'VARCHAR'),
        ('CustomerName', 'VARCHAR'),
        ('ShippingAddressId',
         "VARCHAR COMMENT 'REFERENCES shipping_addresses (address_id)'"),
        ('InvoiceAddressId',
         "VARCHAR COMMENT 'REFERENCES shipping_addresses (address_id)'"),
        ('Site', 'VARCHAR'),
        ('Warehouse', 'VARCHAR'),
        ('OwnerId', 'VARCHAR'),
        ('StockStatus', 'VARCHAR'),
        ('SalesOrder', 'VARCHAR'),
        ('Prime', 'VARCHAR'),
        ('PriorityAllocation', 'VARCHAR'),
        ('PriorityDespatch', 'VARCHAR'),
        ('CustomerRef', 'VARCHAR'),
        ('ConsigmentId', 'VARCHAR'),
        ('PickGroupId', 'VARCHAR'),
        ('ASNNumber', 'VARCHAR'),
        ('DNoteNumber', 'VARCHAR'),
        ('InvoiceNumber', 'VARCHAR'),
        ('ManifestNumber', 'VARCHAR'),
        ('POD', 'VARCHAR'),
        ('ShippingMethod', 'VARCHAR'),
        ('Region', 'VARCHAR'),
        ('CarrierId', 'VARCHAR'),
        ('CarrierTrackingNumber', 'VARCHAR'),
        ('Route', 'VARCHAR'),
        ('LoadId', 'VARCHAR'),
        ('LoadSequence', 'INTEGER'),
        ('PackStation', 'VARCHAR'),
        ('ShippingLane', 'VARCHAR'),
        ('ReturnReason', 'VARCHAR'),
        ('QC', 'VARCHAR'),
        ('Lines', 'INTEGER'),
        ('LineQty', 'INTEGER'),
        ('StUQty', 'INTEGER'),
        ('Volume', 'NUMBER(10, 6)'),
        ('Weight', 'NUMBER(10, 3)'),
        ('ActualWeight', 'NUMBER(10, 6)'),
        ('TaskCountNew', 'INTEGER'),
        ('TaskCountCurrent', 'INTEGER'),
        ('TaskCountActioned', 'INTEGER'),
        ('TimeToPick', 'NUMBER(10, 3)'),
        ('TimeToPack', 'NUMBER(10, 3)'),
        ('TimeToCheck', 'NUMBER(10, 3)'),
        ('TimeToLoad', 'NUMBER(10, 3)'),
        ('TimeOther', 'NUMBER(10, 3)'),
        ('TimeToDeliver', 'NUMBER(10, 3)'),
        ('InvoiceInd', 'VARCHAR'),
        ('Currency', 'VARCHAR'),
        ('LineValue', 'NUMBER(10, 3)'),
        ('Discount', 'NUMBER(10, 3)'),
        ('Packing', 'NUMBER(10, 3)'),
        ('Freight', 'NUMBER(10, 3)'),
        ('Insurance', 'NUMBER(10, 3)'),
        ('Charges', 'NUMBER(10, 3)'),
        ('Allowances', 'NUMBER(10, 3)'),
        ('Tax', 'NUMBER(10, 3)'),
        ('InvoiceValue', 'NUMBER(10, 3)'),
        ('ShortageCode', 'VARCHAR'),
        ('Variance', 'VARCHAR'),
        ('CutOffInd', 'VARCHAR'),
        ('Supervisor', 'VARCHAR'),
        ('Reason', 'VARCHAR'),
        ('DateCreated', 'TIMESTAMP_NTZ'),
        ('DateSuspended', 'TIMESTAMP_NTZ'),
        ('DateClosed', 'TIMESTAMP_NTZ'),
        ('DateDueOut', 'TIMESTAMP_NTZ'),
        ('DateShipment', 'TIMESTAMP_NTZ'),
        ('DateDelivery', 'TIMESTAMP_NTZ'),
        ('DateInvoice', 'TIMESTAMP_NTZ'),
        ('ASNInd', 'VARCHAR'),
        ('OverdueInd', 'VARCHAR'),
        ('Stage', 'VARCHAR'),
        ('MaintInd', 'VARCHAR'),
    )


class ExtTable(Table):
    _flatten_array = None

    @property
    def from_clause(self):
        sup = super().from_clause
        return f"""
            {sup},
            LATERAL FLATTEN(INPUT => _shipments.value,
                            PATH => '{self._flatten_array}') _{self.name}
        """

    @property
    def constraint(self):
        keys = self.parenthesize(c for c, _ in self.column_spec[:2])
        return f'PRIMARY KEY {keys}'


@export(tables)
class ShipmentLines(ExtTable):
    name = 'shipment_lines'
    _flatten_array = 'ShipmentLines'
    column_spec = (
        ('Line', 'VARCHAR'),
        ('ShipmentId', 'VARCHAR NOT NULL REFERENCES shipments (ShipmentId)'),
        ('Level', 'VARCHAR'),
        ('SKUId', 'VARCHAR'),
        ('BizSKU', 'VARCHAR'),
        ('UnitOfMeasure', 'VARCHAR NOT NULL'),
        ('LineOwner', 'VARCHAR'),
        ('LineStockStatus', 'VARCHAR'),
        ('QtyOrdered', 'INTEGER NOT NULL'),
        ('QtyRequired', 'INTEGER'),
        ('QtyAllocated', 'INTEGER'),
        ('QtyTasked', 'INTEGER'),
        ('QtyPicked', 'INTEGER'),
        ('QtyShipped', 'INTEGER'),
        ('QtyDelivered', 'INTEGER'),
        ('QtyDueOut', 'INTEGER'),
        ('Price', 'NUMBER(10, 2)'),
        ('Discount', 'NUMBER(10, 2)'),
        ('TaxRate', 'NUMBER(10, 4)'),
        ('SOLineId', 'INTEGER'),
        ('ReturnReason', 'VARCHAR'),
        ('QC', 'VARCHAR'),
        ('Shortage', 'VARCHAR'),
        ('Variance', 'VARCHAR'),
        ('BOInd', 'VARCHAR'),
        ('ConsignmentId', 'VARCHAR'),
        ('PickGroupId', 'VARCHAR'),
        ('SiteId', 'VARCHAR'),
        ('Warehouse', 'VARCHAR'),
        ('BizId', 'VARCHAR'),
        ('OwnerId', 'VARCHAR'),
        ('StockStatus', 'VARCHAR'),
        ('DateShipment', 'TIMESTAMP_NTZ'),
        ('AttachmentInd', 'VARCHAR'),
        ('SpecialConditionInd', 'VARCHAR'),
        ('Stage', 'VARCHAR'),
    )
    constraints = 'PRIMARY KEY (Line, ShipmentId)'


@export(tables)
class ShipmentAddresses(ExtTable):
    name = 'shipment_addresses'
    _flatten_array = 'ShipAddress'
    column_spec = (
        ('AddressId', 'VARCHAR PRIMARY KEY'),  # from scruffy, ergo unique
        ('ShipmentId', 'VARCHAR NOT NULL REFERENCES shipments (ShipmentId)'),
        ('Name', 'VARCHAR NOT NULL'),
        ('Line1', 'VARCHAR NOT NULL'),
        ('Line2', 'VARCHAR'),
        ('Line3', 'VARCHAR'),
        ('City', 'VARCHAR'),
        ('State', 'VARCHAR'),
        ('Postcode', 'VARCHAR'),
        ('Country', 'VARCHAR'),
        # the spec states Country is "mandatory", but it does sometimes show as
        # null at least in UAT data: hence we mark it nullable in the table
        ('Region', 'VARCHAR'),
        ('Latitude', 'NUMBER(10, 6)'),
        ('Longitude', 'NUMBER(10, 6)'),
    )


@export(tables)
class ShipmentContacts(ExtTable):
    name = 'shipment_contacts'
    _flatten_array = 'ShipContacts'
    column_spec = (
        ('ShipmentId', 'VARCHAR NOT NULL'),
        ('LineId', 'VARCHAR NOT NULL'),
        ('Title', 'VARCHAR'),
        ('FirstName', 'VARCHAR'),
        ('LastName', 'VARCHAR'),
        ('Salutation', 'VARCHAR'),
        ('Position', 'VARCHAR'),
        ('Email', 'VARCHAR'),
        ('Fax', 'VARCHAR'),
        ('Phone', 'VARCHAR'),
        ('Mobile', 'VARCHAR'),
        ('Pager', 'VARCHAR'),
        ('Language', 'VARCHAR'),
    )
    constraints = 'PRIMARY KEY (ShipmentId, LineId)'
