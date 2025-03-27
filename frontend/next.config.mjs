/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "img.daisyui.com",
        // port: "",
        // pathname: "/account123/**",
        // search: "",
      },
    ],
  },
};

export default nextConfig;
