import DocumentUploader from '@/components/DocumentUploader';
import Head from 'next/head';

export default function HomePage() {
  return (
    <div>
      <Head>
        <title>Book Reading Bot</title>
      </Head>
      <DocumentUploader></DocumentUploader>
    </div>
  );
}