using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Denombrements 
/**
* titre : Denombrements 
* description : Programme effectuant une Permutation ou Arrangement ou Combinaison.
* auteur : hammou brahim
* date création : 06/01/2023
* date dernière modification : 06/01/2023
*/
{
    class Program
    {
        static void Main(string[] args)
        {
            int c = 1; // Initialisation du choix
            
                Console.WriteLine("Permutation ...................... 1");
                Console.WriteLine("Arrangement ...................... 2");
                Console.WriteLine("Combinaison ...................... 3");
                Console.WriteLine("Quitter .......................... 0");
                Console.Write("Choix :                            ");
                c = int.Parse(Console.ReadLine());
                if (c == 0) 
                { 
                Environment.Exit(0); 
                }
                else if (c == 1)
                {
                    Console.Write("nombre total d'éléments à gérer = "); // le nombre d'éléments à gérer
                    int n = int.Parse(Console.ReadLine()); // saisir le nombre
                                                           // calcul de r
                    long Reponse = 1;
                    for (int k = 1; k <= n; k++)
                        Reponse *= k;
                    Console.WriteLine(n + "! = " + Reponse);
                }
                else if (c == 2)
                {
                        Console.Write("nombre total d'éléments à gérer = "); // le nombre d'éléments à gérer
                        int t = int.Parse(Console.ReadLine()); // saisir le nombre
                        Console.Write("nombre d'éléments dans le sous ensemble = "); // le sous ensemble
                        int n = int.Parse(Console.ReadLine()); // saisir le nombre
                        // calcul de r
                        long Reponse = 1;
                        for (int k = (t - n + 1); k <= t; k++)
                            Reponse *= k;
                        //Console.WriteLine("résultat = " + (r1 / r2));
                        Console.WriteLine("A(" + t + "/" + n + ") = " + r);
                }
                else


                {
                        Console.Write("nombre total d'éléments à gérer = "); // le nombre d'éléments à gérer
                        int t = int.Parse(Console.ReadLine()); // saisir le nombre
                        Console.Write("nombre d'éléments dans le sous ensemble = "); // le sous ensemble
                        int n = int.Parse(Console.ReadLine()); // saisir le nombre
                        // calcul de r1
                        long Reponse1 = 1;
                        for (int k = (t - n + 1); k <= t; k++)
                            Reponse1 *= k;
                        // calcul de r2
                        long Reponse2 = 1;
                        for (int k = 1; k <= n; k++)
                            Reponse2 *= k;
                        // calcul de r3
                        //Console.WriteLine("résultat = " + (r1 / r2));
                        Console.WriteLine("C(" + t + "/" + n + ") = " + (Reponse1 / Reponse2));

                /// On propose 3 choix pour les 3 tirages differents, on utilise 4 if le premier étant la fermeture du programme.
                /// Ensuite on va dans chaque cas demander les parametres voulus puis calculer la réponse sur d'autres variables r. On garde nos parametres pour pouvoir les réutiliser.
                /// On affiche le résultat.


                }  
            Console.ReadLine();
        }
    }
}
