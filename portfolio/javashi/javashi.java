import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class javashi {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Zadej své uživatelské jméno: ");
        String username = scanner.nextLine();

        System.out.print("Zadej své heslo: ");
        String password = scanner.nextLine();

        System.out.print("sluzba pro kterou budete pouzivat toto heslo: ");
        String service = scanner.nextLine();

        try (FileWriter writer = new FileWriter("someshi.txt", true)) {
            writer.write("\n" + "username" + "   " + "password" + "   " + "servise" + "\n" + username + "   " + password + "   " + service + "\n");
            System.out.println("Úspěšně uloženo do souboru 'someshi.txt'.");
        } catch (IOException e) { //error catch (ioexception bla bla)
            System.out.println("Chyba při zápisu do souboru: " + e.getMessage());
        }

        scanner.close();
    }
}
