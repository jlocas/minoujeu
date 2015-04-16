using UnityEngine;
using System.Collections;

public class Cheese : MonoBehaviour {
	
	public Vector3 initScale = new Vector3(0.1f,0.1f,0.1f);
	public Vector3 targetScale = new Vector3(50,50,50);
	public float ripenSpeed = 1;
	private float spawnTime;
	private float scaleDifference;
	public bool isReady = false;
	//public bool isClaimed = false;

	public int id = 0;



	// Use this for initialization
	void Start () {
		gameObject.transform.localScale = initScale;
		spawnTime = Time.time;
		scaleDifference = Vector3.Distance(initScale, targetScale);
	
	}
	
	// Update is called once per frame
	void Update () {
		if (!Ripe()){
			Ripen ();	
		} else {
			Fall ();
		}

	}

	void Ripen(){
		float ripenProgress = (Time.time - spawnTime) * ripenSpeed;
		float ripenFrac = ripenProgress / scaleDifference;
		gameObject.transform.localScale = Vector3.Lerp(initScale, targetScale, ripenFrac);

	}

	void Fall(){
		gameObject.GetComponent<Rigidbody>().useGravity = true;
		isReady = true;
	}

	public bool Ripe(){
		if(gameObject.transform.localScale == targetScale){
			return true;
		} else {
			return false;
		}
	}

}
