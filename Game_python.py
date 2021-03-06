import json
import os

from decimal import Decimal


#from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def get(event):
    table = dynamodb.Table("Game_data")

    # fetch todo from the database
    
    result = table.get_item(
        Key={'email' : event['email'],'gametime' : event['gametime']}
    )

    return result['Item']

def get_bad_week(event):
    table = dynamodb.Table("Bad_week")

    # fetch todo from the database
    
    result = table.get_item(
        Key={'email': "badweek",'gametime': event['gametime']}
    )
    print(event)
    
    print(result)

    return result['Item']

def rl_open(user_rate):
    rl=['rack','last','opaque','gov']
    rl_fl={}
    for r in rl:
        if user_rate['K_'+r+'_Price']==None:
            rl_fl[r]=0
        else:
            rl_fl[r]=1
    return rl_fl

def calc_spread_gov(event):
    user_rate=get(event)
    level_closure=rl_open(user_rate)
    badweek_data=get_bad_week(event)
    perc={"K_rack_Per": 0.08,"K_last_Per": 0.14,"K_opaque_Per": 0.08,"K_gov_Per": 0.42,"Q_rack_Per": 0.06,"Q_last_Per": 0.71,"Q_opaque_Per": 0.18,"Q_gov_Per": 0.06,"S_rack_Per": 0.2,"S_last_Per": 0.2,"S_opaque_Per": 0.6,"S_gov_Per": 0}
    room_types=['K','Q','S']
    total_sold=sold_step_1(event)
    sold={}
    for r in room_types:
        if level_closure['gov']==0:
            sold[r+'_gov_Sold']=int(0)
        elif user_rate[r+'_gov_Price']>=user_rate[r+'_rack_Price']:
            sold[r+'_gov_Sold']=int(0)
        elif level_closure['gov']==1 and user_rate[r+'_gov_Price']<user_rate[r+'_rack_Price']:
            sold[r+'_gov_Sold']=min(total_sold[r],int(badweek_data[r+'_gov']))
        total_sold[r]=total_sold[r]-sold[r+'_gov_Sold']
        if level_closure['last']==0:
            sold[r+'_last_Sold']=int(0)
        else:
            sold[r+'_last_Sold']=min(total_sold[r],int((level_closure['last']*perc[r+'_last_Per'])/((level_closure['last']*perc[r+'_last_Per'])+(level_closure['opaque']*perc[r+'_opaque_Per'])+(level_closure['gov']*perc[r+'_gov_Per']))))
        total_sold[r]=total_sold[r]-sold[r+'_last_Sold']
        if level_closure['opaque']==0:
            sold[r+'_opaque_Sold']=int(0)
        else:
            sold[r+'_opaque_Sold']=min(total_sold[r],int((level_closure['opaque']*perc[r+'_opaque_Per'])/((level_closure['last']*perc[r+'_last_Per'])+(level_closure['opaque']*perc[r+'_opaque_Per'])+(level_closure['gov']*perc[r+'_gov_Per']))))
        total_sold[r]=total_sold[r]-sold[r+'_opaque_Sold']
        if level_closure['rack']==0:
            sold[r+'_rack_Sold']=int(0)
        else:
            sold[r+'_rack_Sold']=int(total_sold[r])
    print(sold)
    return sold
    
def prob_adj_1(level_closure):
    if level_closure['rack']==0:
        return -1
    elif level_closure['opaque']==0 and level_closure['gov']==0:
        return -0.08
    elif level_closure['opaque']==0:
        return -0.05
    elif level_closure['gov']==0:
        return -0.03
    else:
        return 0 

def prob_calc(event,BW_LRA,comp_LRA):
    prob_diff=(BW_LRA/comp_LRA[str(event['gametime'])])-1
    user_rate=get(event)
    level_closure=rl_open(user_rate)
    start_range=[-1,-0.25,-0.15,-0.03,0,0.05,0.15,0.25,0.50]
    prob_adj_2=[0.48,0.24,0.08,0,-0.1,-0.25,-0.5,-0.75,-1]
    for index,i in enumerate(start_range):
        if prob_diff>i:
            sel_index=index
        else:
            break
    prob=0.25*(1+prob_adj_1(level_closure))*(1+prob_adj_2[sel_index])
    return prob

def sold_step_1(event):
    md={'6':[0,0,0],'8':[4,8,4],'10':[8,8,4],'12':[0,4,0],'14':[0,8,0],'16':[4,12,0],'18':[4,8,4],'20':[16,16,8],'22':[4,4,0],'24':[4,0,0]}
    market_demand=md[str(event['gametime'])] #game_time
    user_rate=get(event)
    keys=["S_opaque_Price","K_rack_Price","Q_opaque_Price","K_opaque_Price","S_rack_Price","Q_rack_Price","K_gov_Price","S_gov_Price","Q_gov_Price","S_last_Price","K_last_Price","Q_last_Price"]
    room_types=['K','Q','S']
    BW_LRA={}
    comp_LRA={}
    bw_sold={}
    comp_LRA['K']={'8':88,'10':Decimal(88.6),'12':Decimal(91.3),'14':Decimal(90.6),'16':Decimal(89.6),'18':Decimal(91.3),'20':92,'22':Decimal(93.6),'24':96}
    comp_LRA['Q']={'8':88,'10':Decimal(88.6),'12':Decimal(91.3),'14':Decimal(90.6),'16':Decimal(89.6),'18':Decimal(91.3),'20':92,'22':Decimal(93.6),'24':96}
    comp_LRA['S']={'8':88,'10':Decimal(88.6),'12':Decimal(91.3),'14':Decimal(90.6),'16':Decimal(89.6),'18':Decimal(91.3),'20':92,'22':Decimal(93.6),'24':96}
    for index,i in enumerate(room_types):
        keys1=[i+"_opaque_Price",i+"_last_Price",i+"_rack_Price",i+"_gov_Price"]
        ur = { key: user_rate[key] if user_rate[key]!=None else 100000 for key in keys1 }
        BW_LRA[i]=min(list(ur.values()))

        bw_sold[i]=(int(market_demand[index]*prob_calc(event,BW_LRA[i],comp_LRA[i])))
    print(bw_sold)
    return bw_sold
    
def put_price(event):
    table = dynamodb.Table("Game_data")
    #print(event)
    event = json.loads(json.dumps(event), parse_float=Decimal)
    item={"email" : event['email'],
        'gametime' : event['gametime'],
        'K_rack_Price' : event['K_rack_Price'],
        'K_last_Price' : event['K_last_Price'],
        'K_opaque_Price' : event['K_opaque_Price'],
        'K_gov_Price' : event['K_gov_Price'],
        'Q_rack_Price' : event['Q_rack_Price'],
        'Q_last_Price' : event['Q_last_Price'],
        'Q_opaque_Price' : event['Q_opaque_Price'],
        'Q_gov_Price' : event['Q_gov_Price'],
        'S_rack_Price' : event['S_rack_Price'],
        'S_last_Price' : event['S_last_Price'],
        'S_opaque_Price' : event['S_opaque_Price'],
        'S_gov_Price' : event['S_gov_Price']}
    table.put_item(Item=item)
    
    
        

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    user_encode_data = json.dumps(event, indent=2).encode('utf-8')
    content=user_encode_data
    s3.Object('east1python1', 'newfile.txt').put(Body=content)
    put_price(event)
    res= calc_spread_gov(event)
    table = dynamodb.Table("Game_data")
    #return res
    #print(res)
    # fetch todo from the database
    #ddb_data = json.loads(json.dumps(res), parse_float=Decimal)
    #return ddb_data
    for k in res.keys():
        table.update_item(Key={'email' : event['email'],'gametime' : event['gametime']},AttributeUpdates={k: {'Value': (res[k]),'Action': 'PUT'}})
    


