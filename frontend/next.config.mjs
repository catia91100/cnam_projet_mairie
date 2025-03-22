/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  ...(process.env.NODE_ENV === "production" && {
    assetPrefix: "/mairie",
    basePath: "/mairie",
  }),
};

export default nextConfig;
