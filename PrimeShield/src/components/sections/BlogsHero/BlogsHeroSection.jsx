"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import styles from "./BlogsHeroSection.module.css";

export default function BlogsHeroSection() {
  const heroRef = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

      tl.fromTo(`.${styles.hero}`, { scale: 1.06 }, { scale: 1, duration: 2 });
      tl.fromTo(`.${styles.overlay}`, { opacity: 0.9 }, { opacity: 0.7, duration: 1.6 }, 0);
      tl.fromTo(".blogs-hero-title", { y: 40, opacity: 0, filter: "blur(6px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 1.2 }, 0.5);
      tl.fromTo(".blogs-hero-sub", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9 }, 0.8);
    }, heroRef);

    return () => ctx.revert();
  }, []);

  return (
    <section ref={heroRef} className={styles.hero}>
      <div className={styles.overlay} />
      <div className={`container ${styles.content}`}>
        <p className={`${styles.label} blogs-hero-sub`}>برايم شيلد</p>
        <h1 className={`${styles.title} blogs-hero-title`}>المدونة</h1>
        <p className={`${styles.subtitle} blogs-hero-sub`}>
          أحدث المقالات والأخبار في مجال العزل الهندسي والمقاولات
        </p>
      </div>
    </section>
  );
}
