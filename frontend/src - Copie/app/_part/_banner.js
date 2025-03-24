import Link from "next/link";

function Banner() {
  return (
    <div>
      <ul>
        <li>      
          <Link href={"/"}>
            Home
          </Link>
        </li>
        <li>      
          <Link href={"/inscription"}>
            Inscription
          </Link>
        </li>
      </ul>


    </div>
  );
}

export default Banner;
