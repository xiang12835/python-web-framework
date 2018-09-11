# coding=utf-8


import json

datas = "{\x22channelType\x22:\x22WX\x22,\x22bill_no\x22:\x22201808161608517982942552\x22,\x22channel_transaction_id\x22:\x2250000707922018081605993682084\x22,\x22partition_id\x22:\x22\x22,\x22tradeSuccess\x22:true,\x22id\x22:\x22207567ab-0a2c-4596-8ae8-94f5f8b44ba5\x22,\x22channel_type\x22:\x22WX\x22,\x22app_id\x22:\x221a5a75e1-a798-4cb6-94aa-0579722097b0\x22,\x22retryCounter\x22:0,\x22transaction_id\x22:\x224200000154201808164101930167\x22,\x22retry_counter\x22:0,\x22transaction_fee\x22:10,\x22sub_channel_type\x22:\x22WX_APP\x22,\x22optional\x22:{},\x22is_recharge_consume\x22:false,\x22transaction_type\x22:\x22REFUND\x22,\x22notify_url\x22:\x22http://api.platform.winlesson.com/api/pay/beecloud/refund/notify\x22,\x22transactionId\x22:\x224200000154201808164101930167\x22,\x22transactionType\x22:\x22REFUND\x22,\x22transactionFee\x22:10,\x22recharge_user\x22:\x22\x22,\x22notifyUrl\x22:\x22http://api.platform.winlesson.com/api/pay/beecloud/refund/notify\x22,\x22messageDetail\x22:{\x22transaction_id\x22:\x224200000154201808164101930167\x22,\x22nonce_str\x22:\x22wn9vXQSx6h2xrCAE\x22,\x22out_refund_no\x22:\x224200000154201808164101930167\x22,\x22sign\x22:\x224976156C55CC0D0C83FAFE1185CE606B\x22,\x22return_msg\x22:\x22OK\x22,\x22mch_id\x22:\x221510245281\x22,\x22refund_id\x22:\x2250000707922018081605993682084\x22,\x22cash_fee\x22:\x2210\x22,\x22out_trade_no\x22:\x22201808161608517982942552\x22,\x22coupon_refund_fee\x22:\x220\x22,\x22transactionFee\x22:10,\x22refund_channel\x22:\x22\x22,\x22tradeSuccess\x22:true,\x22appid\x22:\x22wx9eb9f8fe4071cc39\x22,\x22refund_fee\x22:\x2210\x22,\x22total_fee\x22:10,\x22result_code\x22:\x22SUCCESS\x22,\x22coupon_refund_count\x22:\x220\x22,\x22cash_refund_fee\x22:\x2210\x22,\x22return_code\x22:\x22SUCCESS\x22},\x22message_detail\x22:{\x22transaction_id\x22:\x224200000154201808164101930167\x22,\x22nonce_str\x22:\x22wn9vXQSx6h2xrCAE\x22,\x22out_refund_no\x22:\x224200000154201808164101930167\x22,\x22sign\x22:\x224976156C55CC0D0C83FAFE1185CE606B\x22,\x22return_msg\x22:\x22OK\x22,\x22mch_id\x22:\x221510245281\x22,\x22refund_id\x22:\x2250000707922018081605993682084\x22,\x22cash_fee\x22:\x2210\x22,\x22out_trade_no\x22:\x22201808161608517982942552\x22,\x22coupon_refund_fee\x22:\x220\x22,\x22transactionFee\x22:10,\x22refund_channel\x22:\x22\x22,\x22tradeSuccess\x22:true,\x22appid\x22:\x22wx9eb9f8fe4071cc39\x22,\x22refund_fee\x22:\x2210\x22,\x22total_fee\x22:10,\x22result_code\x22:\x22SUCCESS\x22,\x22coupon_refund_count\x22:\x220\x22,\x22cash_refund_fee\x22:\x2210\x22,\x22return_code\x22:\x22SUCCESS\x22},\x22is_recharge\x22:false,\x22trade_success\x22:true,\x22partition_info\x22:\x22\x22,\x22signature\x22:\x22593e23c24546411398bbe52c6141e8f4\x22,\x22sign\x22:\x225788d2c523ab2916cb632a6a0bdec5e7\x22,\x22signAll\x22:\x22aaca7d5aac52c7eace3a59515f9fb938\x22,\x22timestamp\x22:1534407120000}"


json_data = json.loads(datas)

print json_data

r = []

print type(json_data)

for k in json_data.keys():
    r.append(k)

print r





