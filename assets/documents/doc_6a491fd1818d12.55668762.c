/*
 * Clavier_souple.c
 *
 * Created: 13/04/2026 15:29:00
 * Author : Payié Mariane ELOLA | Séphora Maurane BAYALA | Mamadou LATIF HAMANI
 *
 * Nouvelles fonctionnalités :
 *   3 tentatives au maximum puis blocage temporel 
 *   Touche '*' : pour effacer le dernier caractère
 *   Touche '#' : pour annuler la saisie et revenir à l'accueil
 */
#define F_CPU 16000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <string.h>
#include <stdio.h>
/*LCD avec PORT A */
#define LCD_D4  0x01// PA0
#define LCD_D5  0x02// PA1
#define LCD_D6  0x04// PA2
#define LCD_D7  0x08// PA3
#define LCD_RS  0x10// PA4
#define LCD_RW  0x20// PA5
#define LCD_EN  0x40// PA6
#define LCD_LENGTH 16 //16 colonnes
#define LCD_LINES 2 // 2 lignes
/*CONSTANTES TEMPORELLES*/
#define DELAI_ACCUEIL_MS 2000u //durée d'affichage de l'écran d'accueil
#define DELAI_SUCCES_MS 3000u //durée d'affichage du message "Accès autorisé"
#define DELAI_ECHEC_MS 500u //pause après affichage du message "Code incorrect"
#define DELAI_BLOCAGE_S 60u //durée de blocage en secondes (1 minute)
/* CONSTANTES SERRURE*/
#define CODE_LEN 6 //longueur du mot de passe
#define MAX_TENTATIVES 3 //nombre maximum d’essais

const char SECRET_CODE[CODE_LEN + 1] = "123456";   /*mot de passe*/

/*FONCTIONS LCD*/
void Write_Cmd1(unsigned char value)
{
    PORTA &= ~(LCD_EN | LCD_RS | LCD_RW);//désactivation EN + mode commande
    PORTA = (value & 0xF0) >> 4; //envoi quartet haut
    PORTA |= LCD_EN; //impulsion Enable
    _delay_us(5);
    PORTA &= ~LCD_EN;
    _delay_us(5);
}
void Write_Cmd(unsigned char value)
{
    PORTA &= ~(LCD_EN | LCD_RS | LCD_RW); //mode commande
    PORTA = (value & 0xF0) >> 4; //quartet haut
    PORTA |= LCD_EN;
    _delay_us(5);
    PORTA &= ~LCD_EN;
    _delay_us(5);
    PORTA = value & 0x0F;//quartet bas
    PORTA |= LCD_EN;
    _delay_us(5);
    PORTA &= ~LCD_EN;
    _delay_us(5);
}
void init_LCD(void)
{
    DDRA |= LCD_EN | LCD_RS | LCD_RW;//configuration des broches en sortie
    DDRA |= LCD_D4 | LCD_D5 | LCD_D6 | LCD_D7;//configuration des broches en sortie
    _delay_ms(15);
    Write_Cmd1(0x30);
	_delay_ms(5);
    Write_Cmd1(0x30);
	_delay_us(100);
    Write_Cmd1(0x30);
	_delay_us(50);
    Write_Cmd1(0x20);
	_delay_us(50);
    Write_Cmd(0x28);
	_delay_us(50);  
    Write_Cmd(0x08);
	_delay_us(50);
    Write_Cmd(0x01);
	_delay_ms(2);   
    Write_Cmd(0x06);  
	_delay_us(50);  
    Write_Cmd(0x0C);  
	_delay_us(50);  
}
void Write_Data(unsigned char value)
{
    PORTA &= ~(LCD_EN | LCD_RW);
    PORTA |=  LCD_RS;
    PORTA = ((value & 0xF0) >> 4) | LCD_RS; //RS est positionné avant chaque quartet et préservé tout au long de l'écriture
    PORTA |= LCD_EN;
    _delay_us(100);
    PORTA &= ~LCD_EN;
    _delay_us(100);
    
    PORTA = (value & 0x0F) | LCD_RS;
    PORTA |= LCD_EN;
    _delay_us(100);
    PORTA &= ~LCD_EN;
    _delay_us(100);
}
void Write_LCD(const char *message)
{
    uint8_t i;
    for (i = 0; i < strlen(message); i++)
    {
        Write_Data((unsigned char)message[i]);
        _delay_us(150);
    }
}
void ligne_1(unsigned char col)
{
    Write_Cmd(0x80 + (col - 1));
    _delay_us(50);
}

void ligne_2(unsigned char col)
{
    Write_Cmd(0x80 + 0x40 + (col - 1));
    _delay_us(50);
}
void pos_xy(unsigned char x, unsigned char y)
{
    if (x < 1 || x > LCD_LENGTH || y < 1 || y > LCD_LINES) //éviter les positions invalides
		return;
    if (y == 1) //choix de la ligne 
		ligne_1(x);
    else        
		ligne_2(x);
    _delay_ms(2);
}
void cls_LCD(void)//Efface complètement l’écran LCD et remet le curseur au début
{
    Write_Cmd(0x01);
    _delay_ms(2);
}
#define LED_VERTE   PB0 
#define LED_ROUGE   PB1

void led_init(void)
{
    DDRB  |=  (1 << LED_VERTE) | (1 << LED_ROUGE); //configuration en sortie
    PORTB &= ~((1 << LED_VERTE) | (1 << LED_ROUGE)); //LEDs éteintes au départ
}

void led_verte_on(void)  
{ 
	PORTB |=  (1 << LED_VERTE); 
}
void led_verte_off(void) 
{ 
	PORTB &= ~(1 << LED_VERTE);
}
void led_rouge_on(void)  
{ 
	PORTB |=  (1 << LED_ROUGE); 
}
void led_rouge_off(void) 
{ 
	PORTB &= ~(1 << LED_ROUGE); 
}

// CLAVIER 4×4 SOUPLE avec PORT C
const char keymap[4][4] = {
    {'1','2','3','A'},
    {'4','5','6','B'},
    {'7','8','9','C'},
    {'*','0','#','D'}
};

void kbd_init(void)
{
    DDRC |=  0x0F;   // PC0-PC3 lignes en sortie
    DDRC &= ~0xF0;   // PC4-PC7 colonnes en entrée
    PORTC |=  0xF0;  // activation pull-up 
}

char kbd_get_key(void) //Détection d'une touche pressée
{
    for (uint8_t row = 0; row < 4; row++) //balayage ligne par ligne
    {
        PORTC = (PORTC | 0x0F) & ~(1 << row);//Met toutes les lignes à 1 puis met une seule ligne à 0
        _delay_us(10);
        uint8_t cols = (~PINC) & 0xF0;//Lecture des colonnes puis inversion car pull-up
        if (cols)
        {
            for (uint8_t col = 0; col < 4; col++)
            {
                if (cols & (1 << (col + 4))) //anti-rebond
                {
                    _delay_ms(20);
                    while ((~PINC) & 0xF0); //attendre relâchement de la touche
                    _delay_ms(20);
                    PORTC |= 0x0F; //remettre les lignes
                    return keymap[row][col]; //retourner le caractère
                }
            }
        }
    }
    PORTC |= 0x0F; //aucune touche
    return 0;
}
void afficher_essais(uint8_t restants)//Affiche le nombre d'essais restants sur la ligne 1
{
    char buf[17]; //buffer temporaire pour construire le texte
    pos_xy(1, 1); //positionnement début ligne 1 
    if (restants == 1) //si 1 seul essai restant
        snprintf(buf, sizeof(buf), "Saisie[1 essai] "); 
    else //plusieurs essais restants
        snprintf(buf, sizeof(buf), "Saisie[%u essais]", (unsigned)restants);
    Write_LCD(buf); //affichage final sur LCD
}
void effacer_char_lcd(uint8_t col)//Efface le caractère sur la ligne 2 à la colonne indiquée 
{
    pos_xy(col, 2); //aller à la bonne colonne
    Write_Data(' ');//affiche un espace à la place
}
void blocage_temporel(void)//pour un compte à rebours
{
    uint16_t minutes = DELAI_BLOCAGE_S / 60u;//Conversion secondes en minutes

    led_rouge_on();

    for (uint16_t m = minutes; m > 0; m--)
    {
        char buf[17];
        cls_LCD();//nettoyage écran
        pos_xy(1, 1);//ligne 1 : message principal
        Write_LCD(" ACCES BLOQUE ! ");
        pos_xy(1, 2);//ligne 2 : temps restant
        snprintf(buf, sizeof(buf), "Reessayer: %2umn  ", (unsigned)m);
        Write_LCD(buf);
        /* Attendre 60 secondes (60 × 1000 ms) */
        for (uint8_t s = 0; s < 60; s++)
            _delay_ms(1000);
    }
    led_rouge_off();//à fin du blocage
}
uint8_t kbd_read_code(char *buf, uint8_t essais_restants)
{
    uint8_t idx = 0; //index de saisie
    cls_LCD(); //préparation de l'écran
    afficher_essais(essais_restants);//ligne 1 : affichage essais restants

    /* Ligne 2 vide — les '*' apparaîtront ici */
    pos_xy(1, 2);//Ligne 2 vide/ les '*' apparaîtront ici
    Write_LCD("                ");

    while (1)//boucle infinie :attend la saisie utilisateur
    {
        char k = kbd_get_key();//lecture d’une touche
        if (k == 0) //aucune touche
			continue;
        if (k == '#')//TOUCHE '#' pour annulation complète
        {
            cls_LCD();
            pos_xy(1, 1);
            Write_LCD("   Annulation   ");
            pos_xy(1, 2);
            Write_LCD("  Retour accueil");
            _delay_ms(1500);
            return 0;   //signale l'annulation au main()
        }
        if (k == '*')//TOUCHE '*' pour supprimer le dernier caractère
        {
            if (idx > 0)
            {
                idx--;//revenir d’un caractère
                effacer_char_lcd(idx + 1);   //efface le '*' affiché 
            }
            continue;
        }
        if (idx < CODE_LEN)//éviter de dépasser la taille maximale
        {
            buf[idx] = k;//sauvegarde du vrai caractère
            idx++;
            pos_xy(idx, 2);
            Write_Data('*');//affichage masqué : on montre '*' au lieu du chiffre
        }
        if (idx == CODE_LEN)
        {
            buf[CODE_LEN] = '\0';//ajout du caractère de fin obligatoire pour les chaînes C
            return 1;//succès
        }
    }
}
int main(void)
{
    init_LCD();//Initialisation de l’écran LCD
    kbd_init();//Initialisation du clavier souple
    led_init();//Initialisation des LEDs
    char saisie[CODE_LEN + 1];//tableau qui va contenir le code saisi par l’utilisateur
    uint8_t tentatives = 0;   //compteur d'échecs consécutifs
    while (1)
    {
        //Écran d'accueil 
        cls_LCD();//nettoyage écran
        pos_xy(1, 1);//ligne 1 
        Write_LCD("  CODE SERRURE  ");//titre principal
        pos_xy(1, 2);//ligne 2
        Write_LCD("Entrez le code: ");//demande de saisie
        _delay_ms(DELAI_ACCUEIL_MS);//petite pause avant saisie
        //Saisie
        uint8_t restants = MAX_TENTATIVES - tentatives;//calcul du nombre d’essais restants
        uint8_t complet  = kbd_read_code(saisie, restants);//lecture du code
        if (!complet) //si l’utilisateur appuie sur '#'on recommence directement sans pénalité
			continue;
		//VÉRIFICATION DU CODE
        if (strncmp(saisie, SECRET_CODE, CODE_LEN) == 0)//comparaison entre :code saisi et mot de passe
        {
            //CODE CORRECT
            tentatives = 0;   // réinitialisation du compteur 
            led_rouge_off();//LED rouge éteinte
            led_verte_on();//LED verte allumée
            cls_LCD();
            pos_xy(1, 1);
            Write_LCD(" ACCES AUTORISE ");//message de succès
            pos_xy(1, 2);
            Write_LCD("  Bienvenue !   ");
            _delay_ms(DELAI_SUCCES_MS);//affichage visible quelques secondes
            led_verte_off();
        }
        else
        {
            //CODE INCORRECT 
            tentatives++;//augmentation du compteur d’erreurs
            led_verte_off();//LED verte éteinte
            led_rouge_on();//LED rouge allumée

            if (tentatives >= MAX_TENTATIVES)
            {
                // BLOCAGE 
                tentatives = 0;//remise à zéro du compteur pour la prochaine session
                blocage_temporel();// bloque pendant DELAI_BLOCAGE_S secondes 
                led_rouge_off();//LED rouge éteinte
                //retour accueil après déblocage 
            }
            else
            {
                // Affiche essais restants 
                uint8_t restants_apres = MAX_TENTATIVES - tentatives;//calcul essais restants
                char buf[17];
                cls_LCD();
                pos_xy(1, 1);
                Write_LCD(" Code incorrect ");//affichage message erreur
                pos_xy(1, 2);
                if (restants_apres == 1)
                    snprintf(buf, sizeof(buf), "Plus qu'1 essai!");
                else
                    snprintf(buf, sizeof(buf), "Reste %u essais  ", (unsigned)restants_apres);
                Write_LCD(buf);
                _delay_ms(DELAI_ECHEC_MS);
               
                while (kbd_get_key() == 0);//Attente que l’utilisateur appuie sur une touche avant de continuer
                _delay_ms(50);
            }
        }
    }
}