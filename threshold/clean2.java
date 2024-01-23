import java.io.BufferedReader;
import java.io.FileReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;


public class clean2 {

    private static int COLUMN_INDEX;
    private static String PATH;
    private static String INPUT_PATH;
    private static String OUTPUT_PATH;
    private static String PSEUDOGENES_PATH;

    public static void main(String[] args) {

        readPathFromFile();

        clean("\t", "\t", true);
    }

    public static void readPathFromFile() {
        try (BufferedReader pathReader = new BufferedReader(new FileReader("path.txt"))) {
            PATH = pathReader.readLine();
            INPUT_PATH = PATH + "data.txt";
            OUTPUT_PATH = PATH + "cleaned_data.txt";
            PSEUDOGENES_PATH = PATH + "assets/hgnc_pseudogenes.txt";
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /*
     * Reads file and returns a list of string arrays.
     */
    public static void clean(String input_delimiter, String output_delimiter, boolean hasHeader) {

        // Read and store pseudogenes
        Set<String> pseudogenes = new HashSet<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(PSEUDOGENES_PATH))) {
            String line;
            while ((line = reader.readLine()) != null) {
                pseudogenes.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Read and clean data
        try {
            BufferedReader reader = new BufferedReader(new FileReader(INPUT_PATH));
            BufferedWriter writer = new BufferedWriter(new FileWriter(OUTPUT_PATH));

            String line;
            
            // Skip header line
            if (hasHeader) {
                line = reader.readLine(); 
                writer.write(line.replace(input_delimiter, output_delimiter));
                writer.newLine();
            }

            while ((line = reader.readLine()) != null) {
                String[] row = line.split(input_delimiter);

                if (include(row) && !pseudogenes.contains(row[COLUMN_INDEX])) {
                    writer.write(String.join(output_delimiter, row));
                    writer.newLine();
                }
            }

            reader.close();
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static boolean include(String[] row) {
        String gene = row[COLUMN_INDEX];

        // Removes sequence that starts with "U" followed by one or more digits
        String snRNAPatternRemoved = gene.replaceAll("^U\\d+", ""); 

        // Removes all non-digits
        String digits = gene.replaceAll("[^0-9]", "");

        if ((gene.length() < 1) ||
            (gene.startsWith("LINC")) ||
            (gene.startsWith("LOC")) ||
            (gene.contains("orf")) ||
            (gene.startsWith("RPS")) ||
            (gene.startsWith("RPL")) ||
            (gene.contains("Y_RNA")) ||
            (gene.contains("-")) ||
            (snRNAPatternRemoved.length() < 1) ||
            (gene.contains("snoU")) ||
            (digits.length() >= 5) ||
            (gene.startsWith("MIR")) ||
            (gene.startsWith("RNU")) ||
            (gene.startsWith("SNORD")) || 
            (gene.startsWith("SNORA")) ||
            (gene.startsWith("SCARNA")) ||
            (gene.startsWith("RNA45S")) ||
            (gene.startsWith("RNA28S")) ||
            (gene.startsWith("RNA18S")) ||
            (gene.startsWith("RNA5S"))) {
                System.out.println("Removed: " + gene);

                try {

                    File file = new File("removed_genes.txt");
                    BufferedWriter writer = new BufferedWriter(new FileWriter(file, true));
                    writer.write(gene);
                    writer.newLine(); 
                    writer.close();
                    
                } catch (IOException e) {
                    e.printStackTrace();
                }

                return false;
        }   

        return true;
    }

}
