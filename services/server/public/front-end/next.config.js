// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
    //for exporting
    //output: "export", //was req. for expoeting 100% as static. now swithing to separet ps for this frontend
    output: "standalone",

    reactStrictMode: true,
    //swcMinify: true,//deleted this line because causes warning

    // If you have pages in src/pages-legacy, you might need to configure this
    pageExtensions: ['tsx', 'ts', 'jsx', 'js'],

    // For shadcn/ui and Radix UI compatibility
    transpilePackages: ['lucide-react', 'next-themes'],

    // If you need to support legacy pages in src/pages-legacy
    // You might want to set up rewrites or redirects

    images: {
        domains: [], // Add your image domains here
        unoptimized: true, //REQUIRED for static export
    },

    // If you get CORS errors in development
    async headers() {
        return [
            {
                source: '/:path*',
                headers: [
                    {
                        key: 'Access-Control-Allow-Origin',
                        value: process.env.NODE_ENV === 'development' 
                        ? '*' 
                        : '*', //your website domain
                    },
                ],
            },
        ];
    },
};

module.exports = nextConfig;
