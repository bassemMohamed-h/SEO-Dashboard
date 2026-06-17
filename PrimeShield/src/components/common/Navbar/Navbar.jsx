"use client";

import { useEffect, useRef, useState } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import gsap from "gsap";
import styles from "./Navbar.module.css";
import ContactModal from "../../sections/ContactModal/ContactModal";

export default function Navbar({ menuPages = [] }) {
  const navRef = useRef(null);
  const pathname = usePathname();
  const [openModal, setOpenModal] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const isHome = pathname === "/";

  useEffect(() => {
    gsap.from(navRef.current, {
      opacity: 0,
      y: -16,
      duration: 0.6,
      ease: "power3.out",
    });
  }, []);

  return (
    <>
      <header
        ref={navRef}
        className={`${styles.navbar}`}
      >
        <div className={`container ${styles.inner}`}>
          {/* Logo */}
          <div className={styles.logo}>
            <Link href="/">
              <img src="/assets/navLogo_result.webp" alt="Prime Shield Logo" />
            </Link>
          </div>

          {/* Desktop Nav Links */}
          <nav className={styles.nav}>
            <Link
              href="/"
              className={`${styles.link} ${
                pathname === "/" ? styles.active : ""
              }`}
            >
              الرئيسية
            </Link>

            <Link
              href="/about"
              className={`${styles.link} ${
                pathname === "/about" ? styles.active : ""
              }`}
            >
              من نحن
            </Link>

            <Link
              href="/services"
              className={`${styles.link} ${
                pathname === "/services" ? styles.active : ""
              }`}
            >
              خدماتنا
            </Link>

            <Link
              href="/projects"
              className={`${styles.link} ${
                pathname === "/projects" ? styles.active : ""
              }`}
            >
              المشاريع
            </Link>

            <Link
              href="/certificates"
              className={`${styles.link} ${
                pathname === "/certificates" ? styles.active : ""
              }`}
            >
              الشهادات
            </Link>

            <Link
              href="/contact"
              className={`${styles.link} ${
                pathname === "/contact" ? styles.active : ""
              }`}
            >
              حساباتنا
            </Link>

            <Link
              href="/blogs"
              className={`${styles.link} ${
                pathname.startsWith("/blogs") ? styles.active : ""
              }`}
            >
              المدونة
            </Link>

            {/* Dynamic pages from Wagtail (show_in_menus = true) */}
            {menuPages.map((page) => {
              const slug = page.meta?.slug || page.slug;
              const href = `/${slug}`;
              return (
                <Link
                  key={page.id}
                  href={href}
                  className={`${styles.link} ${
                    pathname === href ? styles.active : ""
                  }`}
                >
                  {page.title}
                </Link>
              );
            })}
          </nav>

          {/* Contact Button (Desktop) */}
          <button
            className={styles.priceBtn}
            onClick={() => setOpenModal(true)}
          >
            تواصل معنا
            <i className="fa-solid fa-headset"></i>
          </button>

          {/* Hamburger (Mobile Only) */}
          <div
            className={`${styles.hamburger} ${menuOpen ? styles.open : ""}`}
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>

        {/* Mobile Menu */}
        {menuOpen && (
          <div className={styles.mobileMenu}>
            <Link href="/" onClick={() => setMenuOpen(false)}>
              الرئيسية
            </Link>

            <Link href="/about" onClick={() => setMenuOpen(false)}>
              من نحن
            </Link>

            <Link href="/services" onClick={() => setMenuOpen(false)}>
              خدماتنا
            </Link>

            <Link href="/projects" onClick={() => setMenuOpen(false)}>
              المشاريع
            </Link>

            <Link href="/certificates" onClick={() => setMenuOpen(false)}>
              الشهادات
            </Link>
            
            <Link href="/contact" onClick={() => setMenuOpen(false)}>
              حساباتنا
            </Link>

            <Link href="/blogs" onClick={() => setMenuOpen(false)}>
              المدونة
            </Link>

            {/* Dynamic pages from Wagtail (show_in_menus = true) */}
            {menuPages.map((page) => {
              const slug = page.meta?.slug || page.slug;
              return (
                <Link
                  key={page.id}
                  href={`/${slug}`}
                  onClick={() => setMenuOpen(false)}
                >
                  {page.title}
                </Link>
              );
            })}

            <button
              className={styles.mobileContactBtn}
              onClick={() => {
                setMenuOpen(false);
                setOpenModal(true);
              }}
            >
              تواصل معنا
              <i className="fa-solid fa-headset"></i>
            </button>
          </div>
        )}
      </header>

      {/* Contact Modal */}
      <ContactModal isOpen={openModal} onClose={() => setOpenModal(false)} />
    </>
  );
}