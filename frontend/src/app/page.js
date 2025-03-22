import Link from "next/link";
function Home() {
  return (
    <div>
      <ul>
        <li>
          <Link href={"/inscription"}>
            Inscription
          </Link>
        </li>
        <li></li>
        <li></li>
      </ul>
    </div>
  );
}

export default Home;

