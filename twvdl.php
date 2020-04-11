<?php
ERROR_REPORTING(E_ALL);
function get_url($url,$headers,$type){
    $ch = curl_init();
    if ($type =='get'){
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET"); 
    } else {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST"); 
    }
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch,CURLOPT_ACCEPT_ENCODING,'');
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    $content = curl_exec($ch);
    return $content;
}

function download_video($url){
    // Get tokens begin
    $vid_id = explode('?',explode('/',$url)[5])[0];
	$video_player_prefix = 'https://twitter.com/i/videos/tweet/';
	$activate_api = 'https://api.twitter.com/1.1/guest/activate.json';
    $headers = ['User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0','accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-language: es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5'];
    $video_response = get_url($video_player_prefix.$vid_id,$headers,'get');
    preg_match('/src=".*.js"/',$video_response,$vid);
    $js_file_content = get_url(explode('"',$vid[0])[1],$headers,'get');
    preg_match('/Bearer ([a-zA-Z0-9%-])+/',$js_file_content,$token);
    array_push($headers,'authorization: '.$token[0]);
    $jsonobj = get_url($activate_api,$headers,'post');
    $obj = json_decode($jsonobj);
    array_push($headers,'x-guest-token:'.$obj->guest_token);
    // Get tokens end
    $twitter_api = 'https://api.twitter.com/1.1/statuses/show.json?id=';
    $jo = get_url($twitter_api.$vid_id,$headers,'get');
    $o = json_decode($jo);
    $media = $o->extended_entities->media;
    $videos = $media[0]->video_info->variants;
    $bitrate = 0;
    foreach($videos as $video){
        if ($video->bitrate){
            if ($video->bitrate > $bitrate){
                $bitrate = $video->bitrate;
                $hq_video_url = $video->url;
            }
        }
    }
    exit($hq_video_url);
}
if (isset($_POST['url'])){
    download_video($_POST['url']);
} else {
    exit('XD');
}
?>