using UnityEngine;
using System.Collections;

public class Mouse : MonoBehaviour {
	OSCSender sound;
	public LevelController lvl;

	public float speedMin;
	public float speedMax;
	public float speed;
	public float acceleration;

	public bool isGoingLeft = true;
	public bool isStopped = false;
	public bool isTurning = false;
	public bool isSetup = false;
	public bool isGoingHome = false;
	public bool gotCheese = false;
	float rotationDamping = 5.0f;
	private Quaternion targetRotation;
	private Vector3 tempPosition;
	
	public GameObject targetCheese;

	private float initTime;
	private Vector3 initPos;
	private Vector3 initPosMouth;
	private float moveDist;
	public GameObject spawnPoint;
	public bool pause = false;
	public float pauseTime;
	public float pauseTimeMin = 1.0f;
	public float pauseTimeMax = 3.0f;

	// Use this for initialization
	void Start () {
		lvl = GameObject.Find("Controls").GetComponent<LevelController>();
		spawnPoint = GameObject.Find("Mouse Spawn Point");
		//mouth = gameObject.transform.FindChild("MouseMouth");
	
	}
	
	// Update is called once per frame
	void Update () {

		//mouse init
		if (targetCheese.GetComponent<Cheese>().isReady && !isSetup){
			isSetup = true;
			sound = GameObject.Find("OSCManager").GetComponent<OSCSender>();
			initTime = Time.time;
			initPos = gameObject.transform.position;
			initPosMouth = gameObject.transform.FindChild("MouseMouth").gameObject.transform.position;
			moveDist = Vector3.Distance(initPos, targetCheese.transform.position);
		}

		//if mouse is ready, then go!
		if (targetCheese.GetComponent<Cheese>().isReady && isSetup){
			MovementAI ();
		}
		gameObject.transform.position = new Vector3(gameObject.transform.position.x, 0, gameObject.transform.position.z);
	
	}

	void MovementAI(){


		if(isTurning){
			Rotate180 ();
		}

		if(pause){
			if (Time.time - initTime < pauseTime){
				return;
			}
			else{
				if(!gotCheese){
					MoveInit(targetCheese);
				} else {
					MoveInit(spawnPoint);
				}
				pause = false;
			}
		}
		if (!gotCheese){
			MoveToTarget(targetCheese);
			if (Vector3.Distance(gameObject.transform.FindChild("MouseMouth").position, targetCheese.transform.position) <= 0.2){
				gotCheese = true;
				targetCheese.GetComponent<Cheese>().Anchor(gameObject.transform.FindChild("MouseMouth").gameObject);
			}
		}
		else {
			MoveToHome();
		}

		if(gotCheese && gameObject.transform.FindChild("MouseMouth").position == spawnPoint.transform.position){
			Destroy(targetCheese);
			Destroy(gameObject);
			lvl.cheeseCount -= 1;
		}

	}


	void MoveToHome(){
		if(isGoingLeft){
			isTurning = true;
		} else if (!isTurning){
			MoveToTarget(spawnPoint);
		}
	}

	void MoveInit(GameObject target){
		initTime = Time.time;
		initPos = gameObject.transform.position;
		initPosMouth = gameObject.transform.FindChild("MouseMouth").gameObject.transform.position;
		moveDist = Vector3.Distance(initPos, target.transform.position);
		speed = speedMin;

	}

	void MoveToTarget(GameObject target){


		if (speed < speedMax){
			float t = (Time.time - initTime) * acceleration / (speedMax-speedMin);
			speed = Mathf.Lerp(speedMin, speedMax, t);
		}
		float moveProgress = (Time.time - initTime) * speed;
		float moveFract = moveProgress / moveDist;
		gameObject.transform.position = Vector3.Lerp(initPosMouth, target.transform.position, moveFract) + initPos - initPosMouth;
	}

	void Rotate180() {

		if (isGoingLeft){
			targetRotation = Quaternion.Euler(0f, 180f, 0f);

		}
		else {
			targetRotation = Quaternion.Euler(0f, 360f, 0f);

		}

		gameObject.transform.rotation = Quaternion.Slerp(gameObject.transform.rotation, targetRotation, Time.deltaTime * rotationDamping);

		if ( Mathf.Abs(gameObject.transform.eulerAngles.y - targetRotation.eulerAngles.y) < 1f ) {
			targetRotation.eulerAngles = new Vector3(0f, Mathf.RoundToInt(targetRotation.eulerAngles.y), 0f);
			gameObject.transform.rotation = targetRotation;
			isTurning = false;
			isGoingLeft = false;
			sound.MouseSqueak();

		}

	}

	public void StopInBush(){
		pause = true;
		pauseTime = Random.Range(pauseTimeMin, pauseTimeMax);
		initTime = Time.time;
	}


}
