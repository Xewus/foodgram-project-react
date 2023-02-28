import React, { useState } from "react";
import api from '../api'

export default function useRecipe () {
  const [ recipe, setRecipe ] = useState({})

  const handleLike = ({ id, toLike = 1 }) => {
    const method = toLike ? api.addToFavorites.bind(api) : api.removeFromFavorites.bind(api)
    method({ id }).then(res => {
      const recipeUpdated = { ...recipe, is_favorited: Number(toLike) }
      setRecipe(recipeUpdated)
    })
    .catch(err => {
      const { errors } = err
      if (errors) {
        alert(errors)
      }
    })
  }

  const handleAddToCart = ({ id, toAdd = 1, callback }) => {
    const method = toAdd ? api.addToOrders.bind(api) : api.removeFromOrders.bind(api)
    method({ id }).then(res => {
      const recipeUpdated = { ...recipe, is_in_shopping_cart: Number(toAdd) }
      setRecipe(recipeUpdated)
      callback && callback(toAdd)
    })
    .catch(err => {
      const { errors } = err
      if (errors) {
        alert(errors)
      }
    })
  }

  const handleSubscribe = ({ author_id, toSubscribe = 1 }) => {
    const method = toSubscribe ? api.subscribe.bind(api) : api.deleteSubscriptions.bind(api)
      method({
        author_id
      })
      .then(_ => {
        const recipeUpdated = { ...recipe, author: { ...recipe.author, is_subscribed: toSubscribe } }
        setRecipe(recipeUpdated)
      })
      .catch(err => {
        const { errors } = err
        if (errors) {
          alert(errors)
        }
      })
  }

  return {
    recipe,
    setRecipe,
    handleLike,
    handleAddToCart,
    handleSubscribe
  }
}
