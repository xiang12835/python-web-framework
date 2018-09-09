#-*- coding: utf-8 -*-  
import json  
import httplib
import logging

#https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/StoreKitGuide/Chapters/Products.html#//apple_ref/doc/uid/TP40008267-CH2-SW7
#https://developer.apple.com/library/ios/documentation/LanguagesUtilities/Conceptual/iTunesConnectInAppPurchase_Guide/Chapters/Introduction.html#//apple_ref/doc/uid/TP40013727
#https://developer.apple.com/library/ios/documentation/LanguagesUtilities/Conceptual/iTunesConnectInAppPurchase_Guide/Chapters/CreatingInAppPurchaseProducts.html#//apple_ref/doc/uid/TP40013727-CH3-SW1


def ios_pay_verify(pay_receipt_data,debug=False,retry=False):
      
    pay_receipt = json.dumps({'receipt-data':pay_receipt_data})
      
    headers = {"Content-type": "application/json"}
    #测试地址  
    if debug:
        connect = httplib.HTTPSConnection("sandbox.itunes.apple.com",timeout=30)
    else:
        connect = httplib.HTTPSConnection("buy.itunes.apple.com",timeout=30)
      
    try:
        connect.request("POST", "/verifyReceipt", pay_receipt, headers)
        result = connect.getresponse()
    except Exception,e:  
        logging.error(e)
        return False, None
      
    if result.status != 200:
        logging.error("POST /verifyReceipt Status:%s" % result.status)
        return False, None
      
    data = result.read()
    connect.close()
    logging.error(data)

    if data:
        decodedJson = json.loads(data)
        status = decodedJson.get('status')

        #测试环境发正式
        if status == 21007 and retry == False:
            d = not debug
            logging.error("21007")
            return ios_pay_verify(pay_receipt_data,debug=d,retry=True)

        #发正环境测试式
        if status == 21008 and retry == False:
            d = not debug
            logging.error("21008")
            return ios_pay_verify(pay_receipt_data,debug=d,retry=True)


        if status == 21002:
            logging.error(pay_receipt_data)

        receipt = decodedJson.get('receipt', {})
          
        transaction_id = receipt.get('transaction_id', '')
        purchase_date = receipt.get('original_purchase_date', '')
        product_id = receipt.get('product_id', '')
        
        if status == 0:
            #返回的status为0时代表支付是成功的，支付成功，最好记录一下  
            return True , receipt
        else:
            logging.error("result verifyReceipt data Status:%s" % status)
          
    return False, None



