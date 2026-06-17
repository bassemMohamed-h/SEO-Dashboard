import Navbar from "@/components/common/Navbar/NavbarWrapper";
import Footer from "@/components/sections/Footer/Footer";
import BlogsHeroSection from "@/components/sections/BlogsHero/BlogsHeroSection";
import BlogsListSection from "@/components/sections/BlogsList/BlogsListSection";
import styles from "./page.module.css";

export const metadata = {
  title: "المدونة",
  description: "أحدث المقالات والأخبار في مجال العزل الهندسي والمقاولات - برايم شيلد",
};

async function getBlogs() {
  try {
    const apiUrl =
      process.env.NEXT_PUBLIC_WAGTAIL_API_URL || "http://127.0.0.1:8000/api/v2";

    const res = await fetch(
      `${apiUrl}/pages/?type=home.BlogPage&fields=date,author,intro,cover_image&order=-date`,
      { cache: "no-store" }
    );

    if (!res.ok) {
      console.error("Failed to fetch blogs:", res.status);
      return [];
    }

    const data = await res.json();
    return data.items || [];
  } catch (err) {
    console.error("Error fetching blogs:", err);
    return [];
  }
}

export default async function BlogsPage() {
  const blogs = await getBlogs();

  return (
    <main className={styles.page}>
      <Navbar />
      <BlogsHeroSection />
      <BlogsListSection blogs={blogs} />
      <Footer />
    </main>
  );
}
