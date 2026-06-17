"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import styles from "./BlogsListSection.module.css";

gsap.registerPlugin(ScrollTrigger);

function formatDate(dateStr) {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  return date.toLocaleDateString("ar-SA", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function BlogCard({ blog, index }) {
  const slug = blog.meta?.slug || blog.slug;
  const coverUrl = blog.cover_image?.url || null;

  return (
    <Link href={`/blogs/${slug}`} className={styles.card}>
      <div className={styles.imageWrapper}>
        {coverUrl ? (
          <img src={coverUrl} alt={blog.title} className={styles.image} />
        ) : (
          <div className={styles.placeholder}>
            <i className="fa-solid fa-newspaper"></i>
          </div>
        )}
        <div className={styles.imageOverlay} />
      </div>

      <div className={styles.body}>
        <div className={styles.meta}>
          {blog.date && (
            <span className={styles.date}>
              <i className="fa-regular fa-calendar"></i>
              {formatDate(blog.date)}
            </span>
          )}
          {blog.author && (
            <span className={styles.author}>
              <i className="fa-regular fa-user"></i>
              {blog.author}
            </span>
          )}
        </div>

        <h2 className={styles.title}>{blog.title}</h2>

        {blog.intro && (
          <p className={styles.intro}>{blog.intro}</p>
        )}

        <span className={styles.readMore}>
          اقرأ المزيد
          <i className="fa-solid fa-arrow-left"></i>
        </span>
      </div>
    </Link>
  );
}

export default function BlogsListSection({ blogs = [] }) {
  const sectionRef = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        `.${styles.card}`,
        { opacity: 0, y: 60 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: "power3.out",
          stagger: 0.12,
          scrollTrigger: {
            trigger: sectionRef.current,
            start: "top 80%",
            toggleActions: "play none none none",
          },
        }
      );
    }, sectionRef);

    return () => ctx.revert();
  }, [blogs]);

  if (blogs.length === 0) {
    return (
      <section ref={sectionRef} className={styles.section}>
        <div className="container">
          <div className={styles.empty}>
            <i className="fa-solid fa-newspaper"></i>
            <p>لا توجد مقالات بعد. ابدأ بإضافة مقالات من لوحة التحكم.</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section ref={sectionRef} className={styles.section}>
      <div className="container">
        <div className={styles.grid}>
          {blogs.map((blog, i) => (
            <BlogCard key={blog.id} blog={blog} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
