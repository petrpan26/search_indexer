import {React, useState} from 'react';
import { Document, Page, pdfjs } from 'react-pdf';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const PDFViewer = ({ file }) => {
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);

    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
        setPageNumber(1);
    }

    function changePage(offset) {
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
            disabled={pageNumber >= numPages}
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