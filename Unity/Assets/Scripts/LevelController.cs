using UnityEngine;
using System.Collections;
using System.Collections.Generic;


public class LevelController : MonoBehaviour {

	public GameObject[] cheeseSpawnPoints;
	public GameObject cheesePrefab;
	private Object newCheese;
	private GameObject tempCheese;
	private GameObject targetCheese;
	public List<Object> allCheeses;
	public float cheeseFrequency;
	public float cheeseTimer = 0.0f;
	public int cheeseCount = 0;
	public int cheeseMax = 2;
	public int cheeseOld;

	public GameObject mouseSpawnPoint;
	public GameObject mousePrefab;
	public Object newMouse;
	public GameObject tempMouse;
	public List<Object> allMice;

	private int spawnPoint;
	private int idCount = 1;


	// Use this for initialization
	void Start () {
		cheeseOld = (int)(Random.value * cheeseSpawnPoints.Length);
	}
	
	// Update is called once per frame
	void Update () {

		cheeseTimer += Time.deltaTime;
		if(cheeseTimer >= cheeseFrequency && cheeseCount < cheeseMax){
			spawnPoint = (int)(Random.value * cheeseSpawnPoints.Length);
			if(spawnPoint != cheeseOld){
				cheeseTimer = 0.0f;
				cheeseCount += 1;
				cheeseOld = spawnPoint;
				SpawnCheese(idCount);
				SpawnMouse(idCount);
				tempMouse.GetComponent<Mouse>().target = tempCheese;
				idCount += 1 % (cheeseMax + 1);
			}
		}



	}

	void SpawnCheese(int id){

		newCheese = Instantiate (cheesePrefab, cheeseSpawnPoints[spawnPoint].transform.position, Random.rotation);
		allCheeses.Add(newCheese);
		tempCheese = (GameObject)allCheeses[allCheeses.Count-1];
		tempCheese.GetComponent<Cheese>().id = id;

	}
	

	/*bool FindCheese(){
		findTimer += Time.deltaTime;
		if (findTimer >= findFrequency){
			findTimer = 0;
			foreach(GameObject cheese in allCheeses){
				if (cheese.GetComponent<Cheese>().isReady == true && cheese.GetComponent<Cheese>().isClaimed == false){
					cheese.GetComponent<Cheese>().isClaimed = true;
					Debug.Log("Cheese found. Mouse on the Hunt. Beware, cheese. You cannot run, cheese.");
					targetCheese = cheese;
					return true;
				}
			}
		}
		return false;
	}*/

	void SpawnMouse(int id){

		newMouse = Instantiate (mousePrefab, mouseSpawnPoint.transform.position, Quaternion.identity);
		allMice.Add(newMouse);
		tempMouse = (GameObject)allMice[allMice.Count-1];
		tempMouse.GetComponent<Mouse>().id = id;


	}

	void DespawnCheese(int id){

		allCheeses.Remove((GameObject)allCheeses[id]);
	}

	void DespawnMouse(int id){

	}
}
