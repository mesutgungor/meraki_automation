#This code reboots meraki devices in an organization
#To run this code you will need an api key and organization id

import meraki
import json
import requests

apikey = 'please_use_your_own_api_key'
myorgId= 'please_put_your_organization_id'
headers = {
        'x-cisco-meraki-api-key': format (str(apikey)),
        'Content-Type': 'application/json'
}
#Get the whole inventory of your organization
orgInventory = meraki.getorginventory (apikey,myorgId)

#This will write whole inventory to a file.
with open('inventory.txt', 'w') as f:
    for item in orgInventory:
        f.write("%s\n" % item)

#en:Below code block will reboot specified model of meraki device and write log to the rebootLog.txt file
start_time = time.time()
counter=0
with open('rebootLogb.txt', 'w') as f:
    f.write ("%s;%s;%s;%s;%s;\n" % ("Date","NetworkID","Name","Model","PublicIP"))
    for item in orgInventory:
        if ('MX65' in item['model'] or 'MX64' in item['model'] or 'MX84' in item['model'] ):
                #posturl = "https://api.meraki.com/api/v0/networks/"+item['networkId']+"/devices/"+item['serial']+"/reboot"
                #dashboard = requests.post(posturl, headers=headers)
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
                counter+=1
                print (str(counter)+' '+timestampStr+' '+item['networkId'] + ', ' + str(item['publicIp'])+ ', ' + item['model'])
                f.write ("%s;%s;%s;%s;%s;\n" % (timestampStr, item['networkId'],item['name'],item['model'],item['publicIp']))

elapsed_time = time.time() - start_time
hours, rem = divmod(elapsed_time, 3600)
minutes, seconds = divmod(rem, 60)
elapsed="{:0>2}h : {:0>2}m : {:05.2f}s".format(int(hours),int(minutes),seconds)
print(str(elapsed_time))
with open('rebootLogb.txt', 'a+') as f:
    f.write("%s Meraki Devices have been rebooted in  %s time"%(counter,elapsed))
