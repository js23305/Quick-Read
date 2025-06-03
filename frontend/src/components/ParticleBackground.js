import React from "react";
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";

export default function ParticleBackground() {
  const particlesInit = async (main) => {
    await loadFull(main);
  };

  return (
    <Particles
      id="tsparticles"
      init={particlesInit}
      options={{
        background: {
          color: "#0a1931",
        },
        fpsLimit: 60,
        interactivity: {
          events: {
            onHover: {
              enable: true,
              mode: "repulse",
            },
            resize: true,
          },
          modes: {
            repulse: {
              distance: 120,
              duration: 0.4,
            },
          },
        },
        particles: {
          color: {
            value: ["#60a5fa", "#38bdf8", "#fff"],
          },
          links: {
            color: "#60a5fa",
            distance: 120,
            enable: true,
            opacity: 0.3,
            width: 1.2,
          },
          move: {
            direction: "none",
            enable: true,
            outModes: {
              default: "bounce",
            },
            random: false,
            speed: 1.2,
            straight: false,
          },
          number: {
            density: {
              enable: true,
              area: 900,
            },
            value: 60,
          },
          opacity: {
            value: 0.7,
          },
          shape: {
            type: "circle",
          },
          size: {
            value: { min: 2, max: 5 },
          },
        },
        detectRetina: true,
        fullScreen: { enable: true, zIndex: 0 },
      }}
    />
  );
}
