create table stock
(
    scode       integer not null,
    companycode integer,
    sname       varchar(20),
    publishname varchar(20),
    mkt         varchar(10),

    primary key (scode)

); --basic stock info
create table hybrid
(
    hycode integer not null,
    scode  integer not null,

    unique (hycode, scode)
); -- hybrid stocks
create table asset
(
    scode             integer not null,
    reportdate        date    not null,
    sumasset          decimal(16, 2),
    fixedasset        decimal(16, 2),
    monetaryfund      decimal(16, 2),
    monetaryfund_tb   decimal(20, 15),
    accountrec        decimal(16, 2),
    accountrec_tb     decimal(20, 15),
    inventory         decimal(16, 2),
    inventory_tb      decimal(20, 15),
    sumliab           decimal(16, 2),
    accountpay        decimal(16, 2),
    accountpay_tb     decimal(20, 15),
    advancereceive    decimal(16, 2),
    advancereceive_tb decimal(20, 15),
    sumshequity       decimal(16, 2),
    sumshequity_tb    decimal(20, 15),
    tsatz             decimal(10, 8),
    tdetz             decimal(10, 8),
    ld                decimal(10, 8),
    zcfzl             decimal(10, 8),

    primary key (scode, reportdate)
); --  assets are time snaps of a stock over a period of time
create table premium
(
    scode                  integer not null,
    reportdate             date    not null,
    cashanddepositcbank    decimal(16, 2),
    cashanddepositcbank_tb decimal(20, 15),
    loanadvances           decimal(16, 2),
    loanadvances_tb        decimal(20, 15),
    saleablefasset         decimal(16, 2),
    saleablefasset_tb      decimal(20, 15),
    borrowfromcbank        decimal(16, 2),
    borrowfromcbank_tb     decimal(20, 15),
    acceptdeposit          decimal(16, 2),
    acceptdeposit_tb       decimal(20, 15),
    sellbuybackfasset      decimal(16, 2),
    sellbuybackfasset_tb   decimal(20, 15),
    settlementprovision    decimal(16, 2),
    settlementprovision_tb decimal(20, 15),
    borrowfund             decimal(16, 2),
    borrowfund_tb          decimal(20, 15),
    agenttradesecurity     decimal(16, 2),
    agenttradesecurity_tb  decimal(20, 15),
    premiumrec             decimal(16, 2),
    premiumrec_tb          decimal(20, 15),
    stborrow               decimal(16, 2),
    stborrow_tb            decimal(20, 15),
    premiumadvance         decimal(16, 2),
    premiumadvance_tb      decimal(20, 15),

    primary key (scode, reportdate)
); --  premium access

alter table hybrid
    add constraint FK_hybrid_to_stock
        foreign key (scode) references stock (scode);

alter table asset
    add constraint FK_asset_to_stock
        foreign key (scode) references stock (scode);

alter table premium
    add constraint FK_premium_to_stock
        foreign key (scode) references stock (scode);

-- test count on stocks issued on bank board
select count(*) banks
from stock
where publishname = '银行'
group by publishname;


-- delete
-- from stock;
-- delete
-- from hybrid;
-- delete
-- from asset;
-- delete
-- from premium;
--
-- drop table stock;
-- drop table hybrid;
-- drop table asset;
-- drop table premium;