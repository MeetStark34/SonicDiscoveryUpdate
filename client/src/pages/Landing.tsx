import { motion } from 'framer-motion';
import { useAuth } from '../hooks/useAuth';

export function Landing() {
    const { login } = useAuth();

    return (
        <div className="h-screen w-full flex flex-col items-center justify-center bg-black relative overflow-hidden">
            {/* Background Glow */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,_rgba(29,185,84,0.15),transparent_50%)]"></div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="z-10 text-center space-y-8"
            >
                <h1 className="text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-500 to-green-300">
                    M.Stark SonicDiscoveryWeb
                </h1>
                <p className="text-xl text-gray-400 font-light tracking-wide">
                    Your Personal AI Music Curator
                </p>

                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={login}
                    className="bg-green-500 text-black font-bold py-4 px-10 rounded-full text-lg shadow-xl shadow-green-500/20 hover:shadow-green-500/40 transition-all"
                >
                    CONNECT WITH SPOTIFY
                </motion.button>
            </motion.div>
        </div>
    );
}
