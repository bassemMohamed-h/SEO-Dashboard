import { notFound } from "next/navigation";
import Navbar from "@/components/common/Navbar/NavbarWrapper";
import Footer from "@/components/sections/Footer/Footer";
import styles from "./page.module.css";
import pageStyles from "../page.module.css";

const API_URL =
  process.env.NEXT_PUBLIC_WAGTAIL_API_URL || "http://127.0.0.1:8000/api/v2";

async function getBlog(slug) {
  try {
    // Step 1: find page ID by slug
    const listRes = await fetch(
      `${API_URL}/pages/?type=home.BlogPage&slug=${slug}`,
      { cache: "no-store" }
    );
    if (!listRes.ok) return null;

    const listData = await listRes.json();
    const item = listData.items?.[0];
    if (!item) return null;

    // Step 2: fetch full detail (all api_fields: body, cover_image, etc.)
    const detailRes = await fetch(`${API_URL}/pages/${item.id}/`, {
      cache: "no-store",
    });
    if (!detailRes.ok) return null;

    return await detailRes.json();
  } catch (err) {
    console.error("Error fetching blog:", err);
    return null;
  }
}

// ImageChooserBlock in StreamField returns only the image ID (integer).
// Resolve each image block to a full download URL via the images API.
async function resolveBodyBlocks(body) {
  if (!body?.length) return [];

  return Promise.all(
    body.map(async (block) => {
      if (block.type === "image" && typeof block.value === "number") {
        try {
          const res = await fetch(`${API_URL}/images/${block.value}/`, {
            cache: "no-store",
          });
          if (res.ok) {
            const img = await res.json();
            // download_url is a relative path like /media/images/...
            // The /media proxy in next.config.mjs serves it via Next.js.
            return { ...block, resolvedUrl: img.meta?.download_url };
          }
        } catch {}
      }
      return block;
    })
  );
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("ar-SA", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const blog = await getBlog(slug);
  if (!blog) return { title: "مقال غير موجود" };
  return {
    title: blog.title,
    description: blog.intro || blog.title,
  };
}

export default async function BlogDetailPage({ params }) {
  const { slug } = await params;
  const blog = await getBlog(slug);
  if (!blog) notFound();

  const body = await resolveBodyBlocks(blog.body);

  // cover_image.url is a relative /media/... path — served via the Next.js proxy
  const coverUrl = blog.cover_image?.url || null;

  return (
    <main className={pageStyles.page}>
      <Navbar />

      {/* Cover hero */}
      <div className={styles.cover}>
        {coverUrl ? (
          <img src={coverUrl} alt={blog.title} className={styles.coverImage} />
        ) : (
          <div className={styles.coverPlaceholder}>
            <i className="fa-solid fa-newspaper"></i>
          </div>
        )}
        <div className={styles.coverOverlay} />
        <div className={`container ${styles.coverContent}`}>
          <div className={styles.metaRow}>
            {blog.date && (
              <span className={styles.metaItem}>
                <i className="fa-regular fa-calendar"></i>
                {formatDate(blog.date)}
              </span>
            )}
            {blog.author && (
              <span className={styles.metaItem}>
                <i className="fa-regular fa-user"></i>
                {blog.author}
              </span>
            )}
          </div>
          <h1 className={styles.title}>{blog.title}</h1>
          {blog.intro && <p className={styles.intro}>{blog.intro}</p>}
        </div>
      </div>

      {/* Article body */}
      <article className={`container ${styles.article}`}>
        {body.map((block, i) => {
          if (block.type === "rich_text") {
            return (
              <div
                key={i}
                className={styles.richText}
                dangerouslySetInnerHTML={{ __html: block.value }}
              />
            );
          }

          if (block.type === "image" && block.resolvedUrl) {
            return (
              <figure key={i} className={styles.figure}>
                <img
                  src={block.resolvedUrl}
                  alt=""
                  className={styles.bodyImage}
                />
              </figure>
            );
          }

          return null;
        })}
      </article>

      <Footer />
    </main>
  );
}
