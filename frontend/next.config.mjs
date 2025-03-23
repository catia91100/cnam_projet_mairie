// /** @type {import('next').NextConfig} */
// const nextConfig = {
//   trailingSlash: true,
//   ...(process.env.NODE_ENV === 'production' && {
//     // assetPrefix: '/mairie',  // Pour servir les assets avec /mairie
//     // basePath: '/mairie',     // Pour que toutes les routes commencent par /mairie
//   }),
// };

// module.exports = nextConfig;



/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  // basePath: "/mairie",
  // assetPrefix: "/mairie",
};

export default nextConfig;
