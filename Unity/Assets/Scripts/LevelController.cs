using UnityEngine;
using System.Collections;
using System.Collections.Generic;


public class LevelController : MonoBehaviour {

	public GameObject[] cheeseSpawnPoints;
	public GameObject cheesePrefab;
	private GameObject newCheese;
	private GameObject targetCheese;

	public float cheeseFrequency;
	public float cheeseTimer = 0.0f;
	public int cheeseCount = 0;
	public int cheeseMax = 2;
	public int cheeseOld;

	public GameObject mouseSpawnPoint;
	public GameObject mousePrefab;
	public GameObject newMouse;

	private int spawnPoint;


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
				SpawnCheese();
				SpawnMouse();
				newMouse.GetComponent<Mouse>().targetCheese = newCheese;
			}
		}




	}

	void SpawnCheese(){

		newCheese = (GameObject)Instantiate (cheesePrefab, cheeseSpawnPoints[spawnPoint].transform.position, Random.rotation);
	}


	void SpawnMouse(){

		newMouse = (GameObject)Instantiate (mousePrefab, mouseSpawnPoint.transform.position, Quaternion.identity);
	}
}
