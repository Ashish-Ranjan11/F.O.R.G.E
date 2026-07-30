import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { ArrowUpRight } from "lucide-react";

export default function ForensicModuleCard({
  title,
  description,
  status,
  icon: Icon,
  onClick,
  index = 0,
}) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const rotateX = useSpring(useTransform(y, [-100, 100], [8, -8]), {
    stiffness: 180,
    damping: 20,
  });

  const rotateY = useSpring(useTransform(x, [-100, 100], [-8, 8]), {
    stiffness: 180,
    damping: 20,
  });

  const handleMouseMove = (event) => {
    const rect = event.currentTarget.getBoundingClientRect();

    x.set(event.clientX - rect.left - rect.width / 2);
    y.set(event.clientY - rect.top - rect.height / 2);
  };

  const resetTilt = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.button
      type="button"
      onClick={onClick}
      onMouseMove={handleMouseMove}
      onMouseLeave={resetTilt}
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.25 }}
      transition={{
        delay: index * 0.1,
        duration: 0.65,
      }}
      style={{
        rotateX,
        rotateY,
        transformStyle: "preserve-3d",
      }}
      className="forge-module-card group relative min-h-[280px] overflow-hidden rounded-[1.75rem] border border-white/10 bg-white/[0.035] p-6 text-left backdrop-blur-2xl"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-red-500/[0.08] via-transparent to-cyan-400/[0.06] opacity-0 transition-opacity duration-500 group-hover:opacity-100" />

      <div className="absolute -right-16 -top-16 h-40 w-40 rounded-full bg-red-500/10 blur-3xl transition-transform duration-700 group-hover:scale-150" />

      <div
        className="relative z-10"
        style={{ transform: "translateZ(38px)" }}
      >
        <div className="flex items-start justify-between">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-black/35 text-red-300 shadow-[0_0_25px_rgba(239,68,68,0.08)]">
            <Icon size={21} />
          </div>

          <div className="flex items-center gap-2 rounded-full border border-emerald-400/15 bg-emerald-400/[0.06] px-3 py-1.5">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,1)]" />
            <span className="text-[8px] uppercase tracking-[0.25em] text-emerald-200/70">
              {status}
            </span>
          </div>
        </div>

        <div className="mt-14">
          <p className="text-[9px] uppercase tracking-[0.32em] text-white/28">
            Forensic Engine 0{index + 1}
          </p>

          <h3 className="mt-3 text-2xl font-semibold tracking-tight text-white">
            {title}
          </h3>

          <p className="mt-3 max-w-xs text-sm leading-6 text-white/42">
            {description}
          </p>
        </div>

        <div className="mt-7 flex items-center justify-between border-t border-white/[0.07] pt-5">
          <span className="text-[9px] uppercase tracking-[0.25em] text-white/35">
            Launch Module
          </span>

          <ArrowUpRight
            size={17}
            className="text-white/35 transition-all duration-300 group-hover:-translate-y-1 group-hover:translate-x-1 group-hover:text-red-300"
          />
        </div>
      </div>
    </motion.button>
  );
}