using UnityEngine;
using System.Collections;

public class Mouse : MonoBehaviour {

	OSCSender sound;
	public LevelController lvl;

	public float speedMin;
	public float speedMax;
	public float speed;
	public float acceleration;

	public GameObject spawnPoint;
	//targetCheese is acquired from an argument of the SpawnMouse() function
	public GameObject targetCheese;
	
	public float rotationDamping = 6.0f;
	public float minAngle = 10.0f;

	public bool gotCheese = false;

	public bool isPaused = false;
	public float pauseTime = 2.0f;
	public float pauseMin = 1.0f;
	public float pauseMax = 10.0f;
	public float pauseStart;

	public float chanceToGoFaster = 0.5f;

	bool gotCheeseTrigger = false;
	bool unpauseTrigger = false;
	bool startTrigger = false;
	

	// Use this for initialization
	void Start () {
		lvl = GameObject.Find("Controls").GetComponent<LevelController>();
		spawnPoint = GameObject.Find("Mouse Spawn Point");
		sound = GameObject.Find("OSCManager").GetComponent<OSCSender>();
		NewSpeed();
	}
	
	// Update is called once per frame
	void Update () {
		Sound ();
		//first check if we are paused in the bush
		if(isPaused){
			if (Time.time - pauseStart < pauseTime){
				return;
			}
			else{
				isPaused = false;
			}
		}
		//if the cheese is ready and we aint got no cheese, move to the cheese
		if(targetCheese.GetComponent<Cheese>().isReady && !gotCheese){
			MoveToPoint(targetCheese.transform.position);
			//Debug.Log("get some chez");

			//if the mouth is close enough, get the cheese and anchor it to the mouth
			if(Vector3.Distance(FindMouth().position, targetCheese.transform.position) <= 0.2){
				//Debug.Log("get some chez");
				gotCheese = true;
				targetCheese.GetComponent<Cheese>().Anchor(FindMouth().gameObject);
			}
		} else if (gotCheese){
			MoveToPoint(spawnPoint.transform.position);
		} 

		if(gotCheese && Vector3.Distance(gameObject.transform.position, spawnPoint.transform.position) <= 0.5){
			Destroy(targetCheese);
			Destroy(gameObject);
			lvl.cheeseCount -= 1;
		}

	
	}
	//main function for movement
	public void MoveToPoint(Vector3 targetPoint){
		float angle = Vector3.Angle(gameObject.transform.forward, targetPoint - gameObject.transform.position);

		//if object is not close to facing the target point:
		if  (angle > minAngle) {
			//Debug.Log("Turning...");

			//rotate the object towards the target point 
			Quaternion rotation = Quaternion.LookRotation(targetPoint - gameObject.transform.position);
			gameObject.transform.rotation = Quaternion.Slerp(gameObject.transform.rotation, rotation, Time.deltaTime * rotationDamping);			
		//if the angle is close enough, start moving but keep rotating
		} else if (angle <= minAngle && angle != 0){
			Quaternion rotation = Quaternion.LookRotation(targetPoint - gameObject.transform.position);
			gameObject.transform.rotation = Quaternion.Slerp(gameObject.transform.rotation, rotation, Time.deltaTime * rotationDamping);

			targetPoint.y = 0;
			float step = speed * Time.deltaTime;
			gameObject.transform.position = Vector3.MoveTowards(gameObject.transform.position, targetPoint, step);

		//if we are facing the target, move towards it
		} else {
			//Debug.Log("Grabbing cheese");

			//to keep the mouse grounded
			targetPoint.y = 0;
			float step = speed * Time.deltaTime;
			gameObject.transform.position = Vector3.MoveTowards(gameObject.transform.position, targetPoint, step);

		}
	}

	public void StopInBush(){
		unpauseTrigger = true;
		isPaused = true;
		pauseTime = Random.Range(pauseMin, pauseMax);
		pauseStart = Time.time;

		if (Random.value <= chanceToGoFaster){
			//chance to add speed after a stop
			GoFaster(1, 4);
		}
	}


	public Transform FindMouth(){
		return gameObject.transform.FindChild("Mesh").transform.FindChild("MouseMouth");
	}

	public void NewSpeed(){
		speed = Random.Range(speedMin, speedMax);
	}

	public void GoFaster(float min, float max){
		speed += Random.Range(min, max);
	}

	public void PlaySqueak(){
		sound.MouseSqueak();
	}

	public void Sound(){
		if (gotCheese && !gotCheeseTrigger){
			PlaySqueak();
			gotCheeseTrigger = true;
		}
		if (!isPaused && unpauseTrigger){
			PlaySqueak();
			unpauseTrigger = false;
		}

		if(targetCheese.GetComponent<Cheese>().isReady && !startTrigger){
			PlaySqueak();
			startTrigger = true;
		}

	}
}
