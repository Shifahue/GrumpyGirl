import React, { useState, useEffect } from 'react';
import { SafeAreaView, View, Text, Button, TextInput, FlatList, TouchableOpacity } from 'react-native';

const BACKEND = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export default function App() {
  const [screen, setScreen] = useState('today');
  const [tasks, setTasks] = useState([]);
  const [newTitle, setNewTitle] = useState('');

  useEffect(() => {
    fetch(`${BACKEND}/api/tasks`).then(r=>r.json()).then(setTasks).catch(()=>{});
  }, [screen]);

  async function createTask(){
    if(!newTitle) return;
    await fetch(`${BACKEND}/api/tasks`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({title: newTitle})
    });
    setNewTitle('');
    setScreen('today');
    fetch(`${BACKEND}/api/tasks`).then(r=>r.json()).then(setTasks).catch(()=>{});
  }

  return (
    <SafeAreaView style={{flex:1, padding:20}}>
      <View style={{flexDirection:'row', justifyContent:'space-between'}}>
        <Button title="Today" onPress={()=>setScreen('today')} />
        <Button title="Capture" onPress={()=>setScreen('capture')} />
        <Button title="Decompose" onPress={()=>setScreen('decompose')} />
      </View>

      {screen === 'today' && (
        <View style={{marginTop:20}}>
          <Text style={{fontSize:18, fontWeight:'bold'}}>Today</Text>
          <FlatList data={tasks} keyExtractor={(i)=>i.id} renderItem={({item})=> (
            <View style={{padding:10, borderBottomWidth:1}}>
              <Text>{item.title}</Text>
              <Text style={{color:'#666'}}>{item.notes || ''}</Text>
            </View>
          )} />
        </View>
      )}

      {screen === 'capture' && (
        <View style={{marginTop:20}}>
          <Text style={{fontSize:18}}>Capture a goal</Text>
          <TextInput value={newTitle} onChangeText={setNewTitle} placeholder="What should I do right now?" style={{borderWidth:1, padding:8, marginTop:10}} />
          <Button title="Create task" onPress={createTask} />
        </View>
      )}

      {screen === 'decompose' && (
        <View style={{marginTop:20}}>
          <Text style={{fontSize:18}}>Decompose</Text>
          <TextInput placeholder="Describe a goal to decompose" style={{borderWidth:1, padding:8, marginTop:10}} onSubmitEditing={(e)=>{
            const goal = e.nativeEvent.text;
            fetch(`${BACKEND}/api/decompose`, {
              method: 'POST',
              headers: {'Content-Type':'application/json'},
              body: JSON.stringify({goal})
            }).then(r=>r.json()).then(j=>alert(JSON.stringify(j)))
          }} />
        </View>
      )}
    </SafeAreaView>
  );
}
