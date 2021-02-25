<?php
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $content = $_GET['ip'];
    $tos = $_GET['weight'];
    $file = $_GET['port'];
    $returns = ['Status'=>'True'];
    $returnd = ['Status'=>'False'];
    if ($tos > '100' or $tos == null){
        header('Content-type: application/json');
        echo json_encode($returnd);
        exit;
    }
    
    if ($tos == '0'){
        $tos = "1 down";
    }

    $cur_time = date('Y-m-d H:i:s',time());
    foreach ($_GET as $key => $value) {
        $p = file_put_contents('/tmp/ngapi.log', $key."\n".$value."\n", FILE_APPEND);
    }
    $l = file_put_contents('/tmp/ngapi.log', "TIME:".$cur_time."\n"."#########################"."\n", FILE_APPEND);
    if (empty($content)){
        header('Content-type: application/json');
        echo json_encode($returnd);
        exit;
    }
    else{
       if (empty($file)){
           $data = explode(',', trim(preg_replace('/[\"\']/', '', $content)));
           foreach ($data as $value){
               if (filter_var($value, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)){
                   if ($value == '10.80.12.137' or $value == '10.80.12.136' or $value == '10.80.11.27' or $value == '10.80.11.29'){
                       $path = "/alidata/nginx/conf/vhosts/[0-9]*.conf";
                       print_r(shell_exec("sed -i '/$value/'d $path"));
                       print_r(shell_exec("sed -i '2{8h;8!h}; 2p' $path"));
                       print_r(shell_exec("sed -i '3s#server [0-9.]*#server $value#' $path"));
                       print_r(shell_exec("sed -i -e '3s/[0-9,a-z];$//' -i -e '3s/[0-9,a-z]$//' -i -e '3s/[0-9,a-z]$//' -i -e '3s/[0-9,a-z]$//' -i -e '3s/[ ]$//'  -i -e '3s/[0-9]$//' -i -e '3s/[0-9]$//' -i -e '3s/[0-9]$//' $path"));
                       print_r(shell_exec("sed -i '3s/$/$tos;/g' $path"));
                       shell_exec("touch /opt/lala");
                  }
                  else{
                      header('Content-type: application/json');
                      echo json_encode($returnd);
                      exit;
                  }
                  }
              else{
                  header('Content-type: application/json');
                  echo json_encode($returnd);         
                  exit;
              } 
          }        
       }   
       else{
           $data = explode(',', trim(preg_replace('/[\"\']/', '', $content)));
           foreach ($data as $value){
               if (filter_var($value, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)){
                   if ($value == '10.80.12.137' or $value == '10.80.12.136' or $value == '10.80.11.27' or $value == '10.80.11.29'){
                      $paths = "/alidata/nginx/conf/vhosts";
                      print_r(shell_exec("sed -i '/$value/'d $paths/$file.conf"));
                      print_r(shell_exec("sed -i 'N;2aserver $value:$file weight=$tos;' $paths/$file.conf"));
                      shell_exec("touch /opt/lala");
               }
               else{
                   header('Content-type: application/json');                                                                                                       
                   echo json_encode($returnd);
                   exit;
               }
               }
               else{
                   header('Content-type: application/json');
                   echo json_encode($returnd);         
                   exit;                
               } 
           }         
       }
       header('Content-type: application/json');
       echo json_encode($returns);   
    }
}else{
        return false;
}
?>
