# GSEA Browser

A web-based interactive browser for Gene Set Enrichment Analysis (GSEA) results visualization. This application allows you to explore and visualize GSEA results with an intuitive interface.

## Features

- Interactive data table with sorting and filtering capabilities
- Gene-based filtering
- Multiple visualization options:
  - Scatter plot
  - Strip plot
  - Dot plot
- Responsive layout that works on both desktop and mobile devices
- Modern and clean user interface

## Installation

You can install the application using either conda or pip:

### Using Conda (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/mohammadalkhatib/gsea_browser.git
cd gsea_browser
```

2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate gsea_browser
```

### Using pip

1. Clone the repository:
```bash
git clone https://github.com/mohammadalkhatib/gsea_browser.git
cd gsea_browser
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Data Structure

The application expects your GSEA results to be organized in the following directory structure:

```
data/
└── project_name/
    └── database_name.csv
```

Each CSV file should contain the following columns:
- term
- es
- nes
- nom p-val
- fdr q-val
- gene %
- lead_genes

## Usage

1. Place your GSEA results in the `data` directory following the structure described above.

2. Run the application:
```bash
python src/app.py
```

3. Open your web browser and navigate to `http://localhost:8050`

4. Use the dropdown menus to:
   - Select a project
   - Choose a database

5. Filter results by entering gene names in the gene filter input (comma-separated)

6. Click on rows in the data table to visualize the lead genes in different plot types

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this tool in your research, please cite:

```
@software{gsea_browser,
  author = {Alkhatib, Mohammad},
  title = {GSEA Browser: Interactive visualization of Gene Set Enrichment Analysis results},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/mohammadalkhatib/gsea_browser}
}
``` 