import React from "react";
import "./Hero.css";
import AnimatedLens from "./AnimatedLens";

export default function Hero() {

  return (
    <section className="hero">

      {/* Background */}
      <div className="ambient ambient-1" />
      <div className="ambient ambient-2" />
      <div className="ambient ambient-3" />
      <div className="ambient ambient-4" />


      {/* Floating words */}
      <div className="hero-word word-witt">
        Witt
      </div>

      <div className="hero-word word-diligence">
        Due Diligence
      </div>

      <div className="hero-word word-innovation">
        Innovation
      </div>


      {/* REAL-TIME WEBGL LENS */}
      <AnimatedLens />

    </section>
  );
}