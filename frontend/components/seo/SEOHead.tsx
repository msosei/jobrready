import { Helmet } from 'react-helmet-async';

interface SEOHeadProps {
  title?: string;
  description?: string;
  keywords?: string;
  image?: string;
  url?: string;
  type?: string;
}

export default function SEOHead({
  title = 'JobBoard Pro - AI-Powered Job Discovery and Career Tools',
  description = 'Find your dream job with intelligent matching, get personalized career insights, and accelerate your professional journey with cutting-edge AI tools.',
  keywords = 'jobs, career, AI, job search, resume, cover letter, interview, hiring',
  image = '/og-image.jpg',
  url = 'https://jobboard-pro.com',
  type = 'website',
}: SEOHeadProps) {
  const fullTitle = title.includes('JobBoard Pro') ? title : `${title} | JobBoard Pro`;

  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <meta name="robots" content="index, follow" />
      <meta name="author" content="JobBoard Pro" />
      <link rel="canonical" href={url} />

      {/* Open Graph Tags */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
      <meta property="og:url" content={url} />
      <meta property="og:site_name" content="JobBoard Pro" />

      {/* Twitter Card Tags */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />

      {/* Additional Meta Tags */}
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="theme-color" content="#3b82f6" />
      <meta name="msapplication-TileColor" content="#3b82f6" />

      {/* Structured Data */}
      <script type="application/ld+json">
        {JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Organization",
          "name": "JobBoard Pro",
          "description": description,
          "url": url,
          "logo": `${url}/logo.png`,
          "sameAs": [
            "https://twitter.com/jobboardpro",
            "https://linkedin.com/company/jobboardpro"
          ]
        })}
      </script>
    </Helmet>
  );
}
