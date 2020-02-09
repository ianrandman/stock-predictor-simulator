export default class Network{
  static  getData = (stock, successCallback, failCallback)=>{
    window.fetch(`https://f4e46a3c-11e7-47e4-92ab-fd169ac7e057.mock.pstmn.io/data?stock=${stock}`).then((resp)=>{
      if(resp.ok){
        resp.text().then((json)=>{
          successCallback(json);
        });
      }else{
        resp.text().then((json)=>{
          failCallback(json);
        });
      }
    })
  };

  static predict = (stock, date, successCallback, failCallback)=>{
    window.fetch(`https://f4e46a3c-11e7-47e4-92ab-fd169ac7e057.mock.pstmn.io/predict?stock=${stock}&date=${date}`).then((resp)=>{
      if(resp.ok){
        resp.text().then((json)=>{
          successCallback(json);
        });
      }else{
        resp.text().then((json)=>{
          failCallback(json);
        });
      }
    })
  }
}