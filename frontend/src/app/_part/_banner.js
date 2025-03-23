import Link from "next/link";

function Banner() {
  return (
    <div>
      <ul>
        <li>      
          <Link href={"/mairie"}>
            Home
          </Link>
        </li>
        <li>      
          <Link href={"/mairie/inscription"}>
            Inscription
          </Link>
        </li>
      </ul>


    </div>
  );
}

export default Banner;
