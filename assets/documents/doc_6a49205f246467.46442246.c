/*
 * DHT11.c
 *
 * Created: 13/04/2026 15:29:00
 * Author : Payié Mariane ELOLA | Sephora Maurane BAYALA | Mamadou LATIF HAMANI
 */ 
#include <avr/io.h>
#define F_CPU 16000000UL
#include "util/delay.h"
#include "C:\Users\HP\Documents\Architecture des calculateurs\lcd_4bits.h"
#include <stdlib.h>
#define dht11 0x10//PB4

unsigned int int_humidite;
unsigned char dec_humidite;
unsigned char int_temperature;
unsigned char dec_temperature;
unsigned char check_sum;
unsigned char tampon, i;
char tamp[2];

void start_dht11(void)
{
	DDRB |= dht11; // ligne de donnée dht11 en sortie
	PORTB &= ~dht11; //impulsion négative d'au moins 18ms sur la ligne dht11
	_delay_ms(20);//
	PORTB |= dht11; //ligne dht11 remise à 1 pour attendre réponse du dht11
	_delay_us(20); // attente de 20µs avant de tester réponse dht11
}
void reponse_dht11(void)
{
	DDRB &= ~dht11; // remise de la ligne dht11 en entrée
	while(PINB & dht11); //ligne à 1?: attendre
	while((PINB & dht11) == 0); //ligne à 0 ?: début de la réponse, attendre.
	while(PINB & dht11); //ligne à 1: fin de réponse: attendre jusqu'à debutde transmission
}
unsigned char Transmission_dht11(void) // récupération des données par octet
{
	for (i=0; i<8; i++)
	{
		while((PINB & dht11) == 0); //début du bit: ligne à 0 pendant 50µs
		//lorsqu’on arrive ici, la ligne est repassée à 1
		_delay_us(30); //attendre au moins 30µs
		if(PINB & dht11) //bit toujours à 1?
		tampon = (tampon << 1) | (0x01);
		// si oui alors c'est un 1: ecrire1 dans le
		//bit actuel = lsbde l'octet tampon
		else //sinon c'est un 0
		tampon = (tampon << 1);
		//le décalage à gauche du contenu de tampon fait entrer un 0 dans son lsb.
		while(PINB & dht11);// fin du bit?
	}
	return tampon;
}

int main(void)
{
	init_LCD();
	Write_LCD("Humidite=");
	pos_xy(1,2);
	Write_LCD("Temp=");
 
    while (1) 
    {
		start_dht11(); //debut: initialisation de transmission
		reponse_dht11(); //accusé de début
		//lecture de 40 bits de données
		int_humidite= Transmission_dht11(); // 8 premiers bits = 8bit integralRH data
		dec_humidite= Transmission_dht11(); // 8 bits suivants = 8bit  decimalRH data
		int_temperature= Transmission_dht11(); // 8 bits suivants = 8bit integralT data
		dec_temperature= Transmission_dht11(); // 8 bits suivants = 8bit  decimalT data
		check_sum= Transmission_dht11(); // 8 derniers bits = 8bit check sum
		//transmission OK?
		if ((int_humidite+ dec_humidite+ int_temperature+ dec_temperature) != check_sum)
		{
			cls_LCD();
			Write_LCD("erreur donnees");
		}
		else
		{
			//humidité
			dtostrf(int_humidite,2,0,tamp);
			pos_xy(11,1);
			Write_LCD(tamp);
			//inutile d'afficher partie décimale car résolution dt11 = 1% RH
			//température
			dtostrf(int_temperature,2,0,tamp);
			pos_xy(8,2);
			Write_LCD(tamp);
			//inutile d'afficher partie décimale car résolution dt11 = 1°C
			
		}
		_delay_ms(10000);
    }
}

