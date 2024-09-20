zipflaw project
# Zipf's Law Analysis Project

This project analyzes Zipf's Law in language corpora, focusing on both English and Chinese texts. Zipf's Law states that the frequency of any word in a large enough corpus is inversely proportional to its rank in the frequency table.

## Features

1. **Data Processing**: 
   - Crawl data from wikipedia (English and Chinese)
   - Convert traditional Chinese characters to simplified

2. **Statistical Analysis**:
   - Calculates word and character frequencies
   - Computes entropy of character distributions

3. **Visualization**:
   - Plots Zipf's Law distributions for words and characters
   - Generates both normal and logarithmic frequency graphs
   - Creates entropy vs. data scale plots

4. **Language Support**:
   - Supports both English and Chinese text analysis
   - Handles language-specific tokenization and cleaning

5. **Output**:
   - Generates statistical reports on character and word probabilities
   - Saves visualizations as PNG files

## Usage

To run the analysis:

1. Ensure you have the required dependencies installed (numpy, matplotlib, etc.)
2. Prepare your input data with wikipedia_chinese crawl
3. Run the main script with appropriate arguments:

   ```
   python verify.py --crawl_data_path path/to/your/data.json --language [english|chinese]
   ```

4. Check the `image/` directory for generated plots and the console output for statistical information

## Project Structure

- wikipedia_chinese/wikipedia_english: 
    crawl data from wikipedia
- `verify.py`: Main script for running the analysis
- `corpus_statics.py`: Contains functions for calculating corpus statistics


## Results

The project generates several outputs:

1. Zipf's Law frequency plots (normal and logarithmic scales)
2. Entropy vs. data scale plots
3. Console output with character and word statistics

These results help visualize and quantify how well the analyzed corpora adhere to Zipf's Law, and provide insights into the information density of the languages studied.

## Contributors

- yesliu

Feel free to contribute to this project by submitting pull requests or reporting issues.

