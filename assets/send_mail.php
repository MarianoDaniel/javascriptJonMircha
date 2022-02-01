<?php
if (isset($_POST)) {
    error_reporting(0);
    $name = $_POST["name"];
    $email = $_POST["email"];
    $subject = $_POST["subject"];
    $comments = $_POST["comments"];

    $domain = $_SERVER["HTTP_HOST"];
    $to = "avicomariano@gmail.com";
    $subject = "Contacto desde el formulario del sitio $domain:$subject";
    $message = "
    <p>
    Contacto desde el formulario del sitio <b> $domain</b>
    </p>
    <ul>
    <li>Nombre: <b>$name</b></li>   
    <li>Email: <b>$email</b></li>   
    <li>Asunto: $Subject</li>   
    <li>Comentarios: $comments</li>   
    </ul>
    ";

    //en el primer campo especifico la versión "MIME-Version: 1.0\r\n" "r" es un enter "n" es un salto de linea
    //Mime type, los contenidos que se envían dentro de la cabecera, sería la segunda inserción de texto Content-Type:text/html;charset=utf-8 junto a "charset=utf.8 que es cómo lo queremos codificar
    //el tercero ayuda a que no vaya a span ya que le enviamos el remitente
    $headers = "MIME-Version: 1.0\r\n" . "Content-Type:text/html;charset=utf-8\r\n" .
        "From:Envío automático no responder <no-reply@$domain>";
    $send_mail = mail($to, $subject, $message, $headers);

    if ($send_mail) {
        $res = [
            "err" => false,
            "message" => "Tus datos han sido enviados"
        ];
    } else {
        $res = [
            "err" => true,
            "message" => "Error al enviar tus datos. Intenta nuevamente"
        ];
    }
    //header("Access-Control-Allow-Origin:https://jonmircha.com");
    header("Access-Control-Allow-Origin:https:*");
    header('Content-type:aplication/json');
    echo json_encode($res);
    exit;
}
