# Printing at Home

Ian Dennis Miller
2017

## signatures and imprints

A 4-page imposition means 4 pages on a single double-sided sheet of paper (i.e. 2up, 2-sided).  4 sheets per signature produces 16 pages per signature. This is not a 16-page signature; it is a 4x4-page signature. The goal of this process is to create the number of 4x4-page signatures required to print the entire book.

The book is separated into 16-page, 8-leaf signatures (a quaternion).  To determine how many signatures there are, divide total pages by 16.  Each 16-page increment results in a new signature.  There is a cutoff at 112 (7 signatures) and 128 (8 signatures).

References:

- https://en.wikipedia.org/wiki/Bookbinding
- https://www.designersinsights.com/designer-resources/understanding-and-working-with-print/

## rendering PDF as print signatures

Execute `make signatures` to convert `mybook.pdf` into a book.
The result is two PDFs:

- `products/mybook-odd.pdf`
- `products/mybook-even.pdf`

First the odd pages are printed, then the pile is sent through the printer a second time to print the even pages on the other side of the papers.

## printing the book

- set up printer for straight-through printing (no rollers/page flips)
- open odd-page PDF; print all sheets
- as the pages emerge, sort them in ascending order (i.e. 1, 3, 5, 7, ...)
- put printed pile into paper tray in the following way:
    - face paper tray with landscape-oriented book
    - rotate clockwise 90 degrees; it feels "backwards"
    - place into paper cartridge with page 1 (e.g. title page) on top
    - the ink side from the previous print run is on top
- open even-page PDF; print all sheets
- print the no-bleed cover in `./products`
