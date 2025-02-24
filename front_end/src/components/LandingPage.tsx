import { FC } from "react";
import { ConnectButton } from "@razorlabs/razorkit";
import { motion } from "framer-motion";

import Image from "next/image";

const LandingPage: FC = () => {
  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen p-4 text-white bg-black">
      {/* Image positioned at the top-left */}
      <div className="absolute top-0 left-4 m-6 p-2 z-10">
        <Image
          src="/move.png"
          width={140}
          height={140}
          alt="Movement Labs"
          className="w-[90px] md:w-[140px] hidden md:block"
        />
      </div>

      <div className="absolute bottom-0 right-1 p-2 z-10 md:m-0 md:bottom-0">
        <Image
          src="/point.png"
          width={160}
          height={160}
          alt="Movement Labs"
          className="lg:w-[150px] md:w-[130px] hidden md:block"
        />
      </div>

      <motion.h1
        className="text-8xl font-bold mb-6 text-center"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Gfin
      </motion.h1>
      <motion.p
        className="text-xl mb-8 text-center max-w-2xl text-gray-300"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        Your personal Financial agent for Movement ecosystem
      </motion.p>
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <ConnectButton
          className="!bg-gradient-to-r !from-purple-500 !to-blue-500 !text-white !font-semibold !py-4 !px-6 !rounded-full 
             !shadow-lg !hover:shadow-xl !transform !transition-transform !duration-300 
             hover:scale-105 hover:bg-gradient-to-l"
          style={{
            backgroundImage: "linear-gradient(to right, #6b46c1, #4299e1)", // Gradient background
            boxShadow: "0 10px 20px rgba(0, 0, 0, 0.2)", // Shadow effect
            transition: "transform 0.3s ease", // Smooth scaling transition
          }}
        />
      </motion.div>
      <motion.div
        className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <FeatureCard
          title="AI-Powered"
          description="Multiple AI agents collaborate for smarter, data-driven investment decisions tailored to your financial goals."
          icon="🧠"
        />
        <FeatureCard
          title="Secured"
          description="Built with non custodial wallet, ensuring top-tier security for all transactions and data."
          icon="🔒"
        />
        <FeatureCard
          title="Ecosystem-Focused"
          description="Specialized in the Movement blockchain, delivering hyper-relevant insights and strategies for maximum growth."
          icon="🔗"
        />
      </motion.div>
    </div>
  );
};

const FeatureCard: FC<{ title: string; description: string; icon: string }> = ({
  title,
  description,
  icon,
}) => (
  <div className="bg-gray-900 p-6 rounded-lg">
    <div className="text-4xl mb-4">{icon}</div>
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <p className="text-sm text-gray-400">{description}</p>
  </div>
);

export default LandingPage;
