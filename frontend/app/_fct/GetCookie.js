// import { useEffect, useState } from "react";
import Cookies from "js-cookie";

function GetCookie(name) {
  // const [cookieValue, setCookieValue] = useState(null);

  // useEffect(() => {
  const cookie = Cookies.get(name); // Récupérer le cookie
  return cookie || null;
  // setCookieValue(cookie);
  // }, []);
}
export default GetCookie;
