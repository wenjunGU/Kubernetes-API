<?php

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        echo $_SERVER[QUERY_STRING];
        $content = $_POST['content'];
        $tos = $_POST['tos'];
        $sender = new SmsMultiSender(1400008698, "5be82618869b903bbc8eb9258f07dcf4");
        foreach ($_POST as $key => $value) {
                $p = file_put_contents('/tmp/sms.log', $key."\n".$value."\n", FILE_APPEND);
        }
        $phoneNumbers = split(',', $tos);
        $con_1 = str_replace('[',',',$content);
        $con_2 = str_replace(']', ',', $con_1);
        $con_3 = split(',', $con_2);
        $send_array = array_filter($con_3);
        file_put_contents('/tmp/sms_msg.log', $send_array[5].' '.$send_array[3].' '.$send_array[9].' '.$send_array[11]."\n", FILE_APPEND);
        $msg = [$send_array[5],$send_array[3],$send_array[9],$send_array[11]];
        $result = $sender->sendSms("86", $phoneNumbers, $msg);
        $result_log = json_decode(json_encode($result),true);
        $cur_time = date('y-m-d H:i:s', time());
        foreach ($result_log['detail'] as $key => $value) {
                file_put_contents('/tmp/sms_send.log', $cur_time.'----'.$value['mobile'].'-----'.$value['errmsg']."\n",FILE_APPEND);
        }
}else{
        return false;
}
// // 下面的 sdkappid 和 appkey 都是无法使用，开放者实际发送短信时请使用申请的 sdkappid 和 appkey
// $sender = new SmsMultiSender(1400008698, "5be82618869b903bbc8eb9258f07dcf4");
// // 下列手机号码均不存在，请替换成实际存在的
// $phoneNumbers = array("18501775484", "13641884623", "17051216337");
// // 请确保签名和模板审核通过
// $sender->sendSms("86", $phoneNumbers, ['test','test','test','test']);

?>
