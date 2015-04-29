using UnityEngine;
using System.Collections;

public class Cheese : MonoBehaviour {
	OSCSender sound;
	public Vector3 initScale = new Vector3(0.1f,0.1f,0.1f);
	public Vector3 targetScale = new Vector3(50,50,50);
	public float ripenSpeed = 1;
	private float spawnTime;
	private float scaleDifference;
	public bool isReady = false;
	float rdyTimer = 0.0f;
	float[] rdyDelay = new float[2]{3, 6};
	float rdyTime = 4.0f;

	public bool isAnchored = false;
	public GameObject anchor;



	// Use this for initialization
	void Start () {
		sound = GameObject.Find("OSCManager").GetComponent<OSCSender>();
		gameObject.transform.localScale = initScale;
		spawnTime = Time.time;
		scaleDifference = Vector3.Distance(initScale, targetScale);
		rdyTime = Random.Range(rdyDelay[0], rdyDelay[1]);
	
	}
	
	// Update is called once per frame
	void Update () {
		if (!Ripe()){
			Ripen ();	
		} else if (gameObject.GetComponent<Rigidbody>().useGravity != true){
			gameObject.GetComponent<Rigidbody>().useGravity = true;
		} else if (isReady != true){
			rdyTimer += Time.deltaTime;
			if(rdyTimer >= rdyTime){
				isReady = true;
			}
		}

		if(isAnchored){
			gameObject.transform.position = anchor.transform.position;
		}

	}

	void Ripen(){
		float ripenProgress = (Time.time - spawnTime) * ripenSpeed;
		float ripenFrac = ripenProgress / scaleDifference;
		gameObject.transform.localScale = Vector3.Lerp(initScale, targetScale, ripenFrac);

	}


	public bool Ripe(){
		if(gameObject.transform.localScale == targetScale){
			return true;
		} else {
			return false;
		}
	}

	public void Anchor(GameObject anchorer){
		anchor = anchorer;
		isAnchored = true;
		gameObject.GetComponent<MeshCollider>().enabled = false;
	}

}
