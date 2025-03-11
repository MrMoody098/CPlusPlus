import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;

public class ExcelToText {

    public static void main(String[] args) {
        String excelFilePath = "grading_rubric.xlsx"; // Path to your Excel file
        String textFilePath = "grading_rubric.txt";   // Path to your output text file

        try (FileInputStream fis = new FileInputStream(new File(excelFilePath));
             Workbook workbook = new XSSFWorkbook(fis);
             FileWriter writer = new FileWriter(new File(textFilePath))) {

            Sheet sheet = workbook.getSheetAt(0); // Get the first sheet

            // Write header
            writer.write("Grading Rubric:\n");
            writer.write("=" + "=".repeat(50) + "\n\n");

            // Iterate over each row in the sheet
            for (Row row : sheet) {
                // Skip header row
                if (row.getRowNum() == 0) {
                    continue;
                }

                Cell weightCell = row.getCell(0);
                Cell loCell = row.getCell(1);
                Cell lookingForCell = row.getCell(2);
                Cell sizingMinCell = row.getCell(3);
                Cell sizingMaxCell = row.getCell(4);

                String weight = getCellValue(weightCell);
                String lo = getCellValue(loCell);
                String lookingFor = getCellValue(lookingForCell);
                String sizingMin = getCellValue(sizingMinCell);
                String sizingMax = getCellValue(sizingMaxCell);

                // Format the row data
                String line = String.format(
                        "Weight: %s\nLO: %s\nLooking For: %s\nSize (Words Min): %s\nSize (Words Max): %s\n",
                        weight, lo, lookingFor, sizingMin, sizingMax
                );

                // Write to text file
                writer.write(line);
                writer.write("-".repeat(50) + "\n");
            }

            System.out.println("Data extraction complete. Check the output file.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String getCellValue(Cell cell) {
        if (cell == null) {
            return "";
        }

        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue();
            case NUMERIC:
                return String.valueOf(cell.getNumericCellValue());
            case BOOLEAN:
                return String.valueOf(cell.getBooleanCellValue());
            default:
                return "";
        }
    }
}
