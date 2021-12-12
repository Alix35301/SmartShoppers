import names
import datetime
from faker import Faker
import random
import numpy as np
 
import pandas as pd
from sqlalchemy import create_engine, engine
fake = Faker()
engine = create_engine('sqlite:///db.sqlite')


for i in range(10):
    print(names.get_full_name())


def get_random_island():
    engine = create_engine('sqlite:///db.sqlite')
    atoll = pd.read_sql_table("atoll", engine)
    island = pd.read_sql_table("island", engine)
    a = atoll.sample()
    a_code =  a.code.iloc[0]
    a_id = a.id.iloc[0]
    a_atoll = a.name.iloc[0]

    # filter from island
    i = island.loc[island.code == a_code].sample()
    i_id = i.id.iloc[0]
    i_name =  i.name.iloc[0]

    return (a_id,i_id)

def get_dob():
    
    start_date = datetime.date(year=1980, month=1, day=1)
    end_date = datetime.date(year=2002, month=1, day=1)

    return fake.date_between(start_date=start_date, end_date=end_date)

def get_rand_addr():
    engine = create_engine('sqlite:///db.sqlite')
    addr = pd.read_sql_table("addreses", engine)
    return addr.sample().name.iloc[0]




names_ = []
dobs = []
emails = []
atolls = []
islands = []
addresses = []
genders = []


for z in range(1000):
    names_.append(names.get_full_name())
    dobs.append(get_dob())
    while 1:
        e = fake.email()
        if e not in emails:
            emails.append(e)
            break

    a,i = get_random_island()
    atolls.append(a)
    islands.append(i)
    addresses.append(get_rand_addr())
    genders.append(random.choice(["Male","Female"]))

users = pd.DataFrame({
    "email" : emails,
    "name" : names_,
    "dob" : dobs,
    "atoll" : atolls,
    "island" : islands,
    "address" : addresses,
    "gender" : genders

})

users["password"] = 1234


users.to_sql("user", engine, if_exists="append", index=False)



user = pd.read_sql_table("user",engine,parse_dates={'dob':'%Y-%m-%d'})
products = pd.read_sql_table("products", engine)

user_id = []
product = []
qty = []
bought_at = []
start_date = datetime.date(year=2019, month=1, day=1)
end_date = datetime.date(year=2021, month=1, day=1)

items = []

for u in user.id.to_list():
    if random.choice([0,1]) ==1:
        num_p = random.randint(1,98)
        for i in range(num_p):
            p = products.sample().id.iloc[0]
            if p not in items:
                user_id.append(u)
                product.append(p)
                qty.append(random.choice([1,5,2]))
                bought_at.append(fake.date_between(start_date=start_date, end_date=end_date))
        items= []

ph = pd.DataFrame({
        "user_id":user_id,
        "product_id":product,
        "qty":qty,
        "bought_at": bought_at
    })
# ph.to_sql("purchases",engine, if_exists="append", index=False)

for u in ph.user_id.unique():
    print(u,ph.loc[(ph.user_id == u)].product_id.to_list())

import numpy as np
def cousine_similarity(u1, u2):
    try:
        return len(np.intersect1d(u1,u2))/len((np.union1d([u1],u2)))
    except ZeroDivisionError:
        return 0



894
d = ph
c = ph.loc[ph.user_id ==894].product_id.to_list()

for u in d.user_id.unique() and u is not 894:
    print(" ",u)
    t = d.loc[d.user_id == u].product_id.to_list()

    print(cousine_similarity(c,t))
    # break

ph = pd.read_sql_table("purchases",engine)
user_id_t = []
user_id_c = []
score = []

for i, j in enumerate(ph.user_id.unique().tolist()):
    # print(i)
    try:
        t = d.loc[d.user_id == j].product_id.to_list()
        # print(j)
        # print(t)
        for l, m in enumerate(ph.user_id.unique().tolist()):
            uid = ph.user_id.unique().tolist()[l+1]
            w = d.loc[d.user_id == uid].product_id.to_list()
            # print(uid)
            # print(w)
            user_id_t.append(j)
            user_id_c.append(uid)
            score.append(cousine_similarity(t,w))
            
    

    except Exception as e:
        pass

df = pd.DataFrame({
    "user_id_c":user_id_c,
    "user_id_t":user_id_t,
    "score": score
})

