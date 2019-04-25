import requests
def ku_login(username, password):
    with requests.Session() as session:
        payload_login = {
            "form_username" : username,
            "form_password": password,
            "zone":"0"
        }
        headers = {
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "en-US,en;q=0.8,th;q=0.6",
            "Cache-Control" : "max-age=0",
            "Connection" : "keep-alive",
            "Content-Length" : "58",
            "Content-Type" : "application/x-www-form-urlencoded",
            "Host" : "stdregis.ku.ac.th",
            "Origin" : "https://stdregis.ku.ac.th",
            "Referer" : "https://stdregis.ku.ac.th/_Login.php",
            "Upgrade-Insecure-Requests" : "1",
            "User-Agent" : "Mozilla/4.5 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) "
        }
        login = session.post("https://stdregis.ku.ac.th/_Login.php", data=payload_login ,headers=headers)
        checkLogin = "_Member_Information.php" in login.text
        if ( checkLogin ):
            return True
        else :
            return False
