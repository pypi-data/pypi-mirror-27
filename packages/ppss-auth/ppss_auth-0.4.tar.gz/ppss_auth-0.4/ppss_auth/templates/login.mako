<form action="${request.route_url('ppsslogin')}" method="POST">
    
    <input type="text" name="username" placeholder="username">
    <br/>
    <input type="password" name="password" placeholder="password">
    <br/>
    <input type="submit" name="submit" value="entra"/>

    <p>${msg}</p>
</form>