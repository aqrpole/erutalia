/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "export", // 🔴 REQUIRED - to create build of static files, index.html, rest all be dafult
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
}

export default nextConfig
