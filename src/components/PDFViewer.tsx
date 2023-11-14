import React, { useState} from 'react';
import { Document, Page, pdfjs} from 'react-pdf';
import type { PDFDocumentProxy } from 'pdfjs-dist';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

interface Props {
    file: File | null;
  }

const PDFViewer = ({file}: Props) => {
    const [numPages, setNumPages] = useState<number | null>(null);
    const [pageNumber, setPageNumber] = useState<number>(1);

    function onDocumentLoadSuccess(numPages: PDFDocumentProxy) {
        setNumPages(numPages);
        setPageNumber(1);
    }

    function changePage(offset: number) {
        setPageNumber(prevPageNumber => prevPageNumber + offset);
    }

    function previousPage() {
        changePage(-1);
    }

    function nextPage() {
        changePage(1);
    }

    return (
        <>
        <Document
            file={file}
            onLoadSuccess={onDocumentLoadSuccess}
        >
            <Page pageNumber={pageNumber} renderTextLayer={false} renderForms={false} renderAnnotationLayer={false}/>
        </Document>
        <div>
            <p>
            Page {pageNumber || (numPages ? 1 : '--')} of {numPages || '--'}
            </p>
            <button
            type="button"
            disabled={pageNumber <= 1}
            onClick={previousPage}
            >
            Previous
            </button>
            <button
            type="button"
            disabled={numPages == null || pageNumber >= numPages}
            onClick={nextPage}
            >
            Next
            </button>
        </div>
        </>
    );
};

const scrollableContainerStyle = {
  maxHeight: '500px', // Set a maximum height for the scrollable container
  overflowY: 'scroll', // Enable vertical scrolling
};

export default PDFViewer;